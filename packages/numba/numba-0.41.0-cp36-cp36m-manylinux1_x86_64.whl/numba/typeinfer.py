"""
Type inference base on CPA.
The algorithm guarantees monotonic growth of type-sets for each variable.

Steps:
    1. seed initial types
    2. build constraints
    3. propagate constraints
    4. unify types

Constraint propagation is precise and does not regret (no backtracing).
Constraints push types forward following the dataflow.
"""

from __future__ import print_function, division, absolute_import

import operator
import contextlib
import itertools
from pprint import pprint
import traceback
from collections import OrderedDict

from numba import ir, types, utils, config, typing
from .errors import (TypingError, UntypedAttributeError, new_error_context,
                     termcolor, UnsupportedError)
from .funcdesc import qualifying_prefix


class NOTSET: pass

# terminal color markup
_termcolor = termcolor()

class TypeVar(object):
    def __init__(self, context, var):
        self.context = context
        self.var = var
        self.type = None
        self.locked = False
        # Stores source location of first definition
        self.define_loc = None
        # Qualifiers
        self.literal_value = NOTSET

    def add_type(self, tp, loc):
        assert isinstance(tp, types.Type), type(tp)

        if self.locked:
            if tp != self.type:
                if self.context.can_convert(tp, self.type) is None:
                    msg = ("No conversion from %s to %s for '%s', "
                           "defined at %s")
                    raise TypingError(msg % (tp, self.type, self.var,
                                             self.define_loc),
                                      loc=loc)
        else:
            if self.type is not None:
                unified = self.context.unify_pairs(self.type, tp)
                if unified is None:
                    msg = "Cannot unify %s and %s for '%s', defined at %s"
                    raise TypingError(msg % (self.type, tp, self.var,
                                             self.define_loc),
                                      loc=self.define_loc)
            else:
                # First time definition
                unified = tp
                self.define_loc = loc

            self.type = unified

        return self.type

    def lock(self, tp, loc, literal_value=NOTSET):
        assert isinstance(tp, types.Type), type(tp)
        assert not self.locked

        # If there is already a type, ensure we can convert it to the
        # locked type.
        if (self.type is not None and
                self.context.can_convert(self.type, tp) is None):
            raise TypingError("No conversion from %s to %s for "
                              "'%s'" % (tp, self.type, self.var), loc=loc)

        self.type = tp
        self.locked = True
        if self.define_loc is None:
            self.define_loc = loc
        self.literal_value = literal_value

    def union(self, other, loc):
        if other.type is not None:
            self.add_type(other.type, loc=loc)

        return self.type

    def __repr__(self):
        return '%s := %s' % (self.var, self.type or "<undecided>")

    @property
    def defined(self):
        return self.type is not None

    def get(self):
        return (self.type,) if self.type is not None else ()

    def getone(self):
        if self.type is None:
            raise TypingError("Undecided type {}".format(self))
        return self.type

    def __len__(self):
        return 1 if self.type is not None else 0


class ConstraintNetwork(object):
    """
    TODO: It is possible to optimize constraint propagation to consider only
          dirty type variables.
    """

    def __init__(self):
        self.constraints = []

    def append(self, constraint):
        self.constraints.append(constraint)

    def propagate(self, typeinfer):
        """
        Execute all constraints.  Errors are caught and returned as a list.
        This allows progressing even though some constraints may fail
        due to lack of information
        (e.g. imprecise types such as List(undefined)).
        """
        errors = []
        for constraint in self.constraints:
            loc = constraint.loc
            with typeinfer.warnings.catch_warnings(filename=loc.filename,
                                                   lineno=loc.line):
                try:
                    constraint(typeinfer)
                except TypingError as e:
                    e = TypingError(str(e),
                                    loc=constraint.loc,
                                    highlighting=False)
                    errors.append(e)
                except Exception:
                    msg = "Internal error at {con}:\n{sep}\n{err}{sep}\n"
                    e = TypingError(msg.format(con=constraint,
                                               err=traceback.format_exc(),
                                               sep='--%<' + '-' * 76),
                                    loc=constraint.loc,
                                    highlighting=False)
                    errors.append(e)
        return errors


class Propagate(object):
    """
    A simple constraint for direct propagation of types for assignments.
    """

    def __init__(self, dst, src, loc):
        self.dst = dst
        self.src = src
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of assignment at {0}", self.loc,
                               loc=self.loc):
            typeinfer.copy_type(self.src, self.dst, loc=self.loc)
            # If `dst` is refined, notify us
            typeinfer.refine_map[self.dst] = self

    def refine(self, typeinfer, target_type):
        # Do not back-propagate to locked variables (e.g. constants)
        assert target_type.is_precise()
        typeinfer.add_type(self.src, target_type, unless_locked=True,
                           loc=self.loc)


class ArgConstraint(object):

    def __init__(self, dst, src, loc):
        self.dst = dst
        self.src = src
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of argument at {0}", self.loc):
            typevars = typeinfer.typevars
            src = typevars[self.src]
            if not src.defined:
                return
            ty = src.getone()
            if isinstance(ty, types.Omitted):
                ty = typeinfer.context.resolve_value_type(ty.value)
            assert ty.is_precise()
            typeinfer.add_type(self.dst, ty, loc=self.loc)


class BuildTupleConstraint(object):
    def __init__(self, target, items, loc):
        self.target = target
        self.items = items
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of tuple at {0}", self.loc):
            typevars = typeinfer.typevars
            tsets = [typevars[i.name].get() for i in self.items]
            for vals in itertools.product(*tsets):
                if vals and all(vals[0] == v for v in vals):
                    tup = types.UniTuple(dtype=vals[0], count=len(vals))
                else:
                    # empty tuples fall here as well
                    tup = types.Tuple(vals)
                assert tup.is_precise()
                typeinfer.add_type(self.target, tup, loc=self.loc)


class _BuildContainerConstraint(object):

    def __init__(self, target, items, loc):
        self.target = target
        self.items = items
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of list at {0}", self.loc):
            typevars = typeinfer.typevars
            tsets = [typevars[i.name].get() for i in self.items]
            if not tsets:
                typeinfer.add_type(self.target,
                                   self.container_type(types.undefined),
                                   loc=self.loc)
            else:
                for typs in itertools.product(*tsets):
                    unified = typeinfer.context.unify_types(*typs)
                    if unified is not None:
                        typeinfer.add_type(self.target,
                                           self.container_type(unified),
                                           loc=self.loc)


class BuildListConstraint(_BuildContainerConstraint):
    container_type = types.List


class BuildSetConstraint(_BuildContainerConstraint):
    container_type = types.Set


class ExhaustIterConstraint(object):
    def __init__(self, target, count, iterator, loc):
        self.target = target
        self.count = count
        self.iterator = iterator
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of exhaust iter at {0}", self.loc):
            typevars = typeinfer.typevars
            for tp in typevars[self.iterator.name].get():
                # unpack optional
                tp = tp.type if isinstance(tp, types.Optional) else tp
                if isinstance(tp, types.BaseTuple):
                    if len(tp) == self.count:
                        assert tp.is_precise()
                        typeinfer.add_type(self.target, tp, loc=self.loc)
                        break
                    else:
                        raise ValueError("wrong tuple length for %r: "
                                         "expected %d, got %d"
                                         % (self.iterator.name, self.count,
                                            len(tp)))
                elif isinstance(tp, types.IterableType):
                    tup = types.UniTuple(dtype=tp.iterator_type.yield_type,
                                         count=self.count)
                    assert tup.is_precise()
                    typeinfer.add_type(self.target, tup, loc=self.loc)
                    break
            else:
                raise TypingError("failed to unpack {}".format(tp),
                                  loc=self.loc)


class PairFirstConstraint(object):
    def __init__(self, target, pair, loc):
        self.target = target
        self.pair = pair
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of pair-first at {0}", self.loc):
            typevars = typeinfer.typevars
            for tp in typevars[self.pair.name].get():
                if not isinstance(tp, types.Pair):
                    # XXX is this an error?
                    continue
                assert tp.first_type.is_precise()
                typeinfer.add_type(self.target, tp.first_type, loc=self.loc)


class PairSecondConstraint(object):
    def __init__(self, target, pair, loc):
        self.target = target
        self.pair = pair
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of pair-second at {0}", self.loc):
            typevars = typeinfer.typevars
            for tp in typevars[self.pair.name].get():
                if not isinstance(tp, types.Pair):
                    # XXX is this an error?
                    continue
                assert tp.second_type.is_precise()
                typeinfer.add_type(self.target, tp.second_type, loc=self.loc)


class StaticGetItemConstraint(object):
    def __init__(self, target, value, index, index_var, loc):
        self.target = target
        self.value = value
        self.index = index
        if index_var is not None:
            self.fallback = IntrinsicCallConstraint(target, operator.getitem,
                                                    (value, index_var), {},
                                                    None, loc)
        else:
            self.fallback = None
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of static-get-item at {0}", self.loc):
            typevars = typeinfer.typevars
            for ty in typevars[self.value.name].get():
                itemty = typeinfer.context.resolve_static_getitem(
                            value=ty, index=self.index)
                if itemty is not None:
                    assert itemty.is_precise()
                    typeinfer.add_type(self.target, itemty, loc=self.loc)
                elif self.fallback is not None:
                    self.fallback(typeinfer)

    def get_call_signature(self):
        # The signature is only needed for the fallback case in lowering
        return self.fallback and self.fallback.get_call_signature()


def fold_arg_vars(typevars, args, vararg, kws):
    """
    Fold and resolve the argument variables of a function call.
    """
    # Fetch all argument types, bail if any is unknown
    n_pos_args = len(args)
    kwds = [kw for (kw, var) in kws]
    argtypes = [typevars[a.name] for a in args]
    argtypes += [typevars[var.name] for (kw, var) in kws]
    if vararg is not None:
        argtypes.append(typevars[vararg.name])

    if not all(a.defined for a in argtypes):
        return

    args = tuple(a.getone() for a in argtypes)

    pos_args = args[:n_pos_args]
    if vararg is not None:
        errmsg = "*args in function call should be a tuple, got %s"
        # Handle constant literal used for `*args`
        if isinstance(args[-1], types.Literal):
            const_val = args[-1].literal_value
            # Is the constant value a tuple?
            if not isinstance(const_val, tuple):
                raise TypeError(errmsg % (args[-1],))
            # Append the elements in the const tuple to the positional args
            pos_args += const_val
        # Handle non-constant
        elif not isinstance(args[-1], types.BaseTuple):
            # Unsuitable for *args
            # (Python is more lenient and accepts all iterables)
            raise TypeError(errmsg % (args[-1],))
        else:
            # Append the elements in the tuple to the positional args
            pos_args += args[-1].types
        # Drop the last arg
        args = args[:-1]
    kw_args = dict(zip(kwds, args[n_pos_args:]))
    return pos_args, kw_args


def _is_array_not_precise(arrty):
    """Check type is array and it is not precise
    """
    return isinstance(arrty, types.Array) and not arrty.is_precise()


class CallConstraint(object):
    """Constraint for calling functions.
    Perform case analysis foreach combinations of argument types.
    """
    signature = None

    def __init__(self, target, func, args, kws, vararg, loc):
        self.target = target
        self.func = func
        self.args = args
        self.kws = kws or {}
        self.vararg = vararg
        self.loc = loc

    def __call__(self, typeinfer):
        msg = "typing of call at {0}\n".format(self.loc)
        with new_error_context(msg):
            typevars = typeinfer.typevars
            with new_error_context(
                    "resolving caller type: {}".format(self.func)):
                fnty = typevars[self.func].getone()
            with new_error_context("resolving callee type: {0}", fnty):
                self.resolve(typeinfer, typevars, fnty)

    def resolve(self, typeinfer, typevars, fnty):
        assert fnty
        context = typeinfer.context

        r = fold_arg_vars(typevars, self.args, self.vararg, self.kws)
        if r is None:
            # Cannot resolve call type until all argument types are known
            return
        pos_args, kw_args = r

        # Check argument to be precise
        for a in itertools.chain(pos_args, kw_args.values()):
            if not a.is_precise():
                # Getitem on non-precise array is allowed to
                # support array-comprehension
                if fnty == operator.getitem and isinstance(pos_args[0], types.Array):
                    pass
                # Otherwise, don't compute type yet
                else:
                    return

        # Resolve call type
        sig = typeinfer.resolve_call(fnty, pos_args, kw_args)

        if sig is None:
            # Note: duplicated error checking.
            #       See types.BaseFunction.get_call_type
            # Arguments are invalid => explain why
            headtemp = "Invalid use of {0} with parameters ({1})"
            args = [str(a) for a in pos_args]
            args += ["%s=%s" % (k, v) for k, v in sorted(kw_args.items())]
            head = headtemp.format(fnty, ', '.join(map(str, args)))
            desc = context.explain_function_type(fnty)
            msg = '\n'.join([head, desc])
            raise TypingError(msg)

        typeinfer.add_type(self.target, sig.return_type, loc=self.loc)

        # If the function is a bound function and its receiver type
        # was refined, propagate it.
        if (isinstance(fnty, types.BoundFunction)
                and sig.recvr is not None
                and sig.recvr != fnty.this):
            refined_this = context.unify_pairs(sig.recvr, fnty.this)
            if refined_this is not None and refined_this.is_precise():
                refined_fnty = fnty.copy(this=refined_this)
                typeinfer.propagate_refined_type(self.func, refined_fnty)

        # If the return type is imprecise but can be unified with the
        # target variable's inferred type, use the latter.
        # Useful for code such as::
        #    s = set()
        #    s.add(1)
        # (the set() call must be typed as int64(), not undefined())
        if not sig.return_type.is_precise():
            target = typevars[self.target]
            if target.defined:
                targetty = target.getone()
                if context.unify_pairs(targetty, sig.return_type) == targetty:
                    sig = sig.replace(return_type=targetty)

        self.signature = sig

        target_type = typevars[self.target].getone()
        if (isinstance(target_type, types.Array)
                and isinstance(sig.return_type.dtype, types.Undefined)):
            typeinfer.refine_map[self.target] = self

    def refine(self, typeinfer, updated_type):
        # Is getitem?
        if self.func == operator.getitem:
            aryty = typeinfer.typevars[self.args[0].name].getone()
            # is array not precise?
            if _is_array_not_precise(aryty):
                # allow refinement of dtype
                assert updated_type.is_precise()
                newtype = aryty.copy(dtype=updated_type.dtype)
                typeinfer.add_type(self.args[0].name, newtype, loc=self.loc)

    def get_call_signature(self):
        return self.signature


class IntrinsicCallConstraint(CallConstraint):
    def __call__(self, typeinfer):
        with new_error_context("typing of intrinsic-call at {0}", self.loc):
            fnty = self.func
            if fnty in utils.OPERATORS_TO_BUILTINS:
                fnty = typeinfer.resolve_value_type(None, fnty)
            self.resolve(typeinfer, typeinfer.typevars, fnty=fnty)


class GetAttrConstraint(object):
    def __init__(self, target, attr, value, loc, inst):
        self.target = target
        self.attr = attr
        self.value = value
        self.loc = loc
        self.inst = inst

    def __call__(self, typeinfer):
        with new_error_context("typing of get attribute at {0}", self.loc):
            typevars = typeinfer.typevars
            valtys = typevars[self.value.name].get()
            for ty in valtys:
                attrty = typeinfer.context.resolve_getattr(ty, self.attr)
                if attrty is None:
                    raise UntypedAttributeError(ty, self.attr,
                                                loc=self.inst.loc)
                else:
                    assert attrty.is_precise()
                    typeinfer.add_type(self.target, attrty, loc=self.loc)
            typeinfer.refine_map[self.target] = self

    def refine(self, typeinfer, target_type):
        if isinstance(target_type, types.BoundFunction):
            recvr = target_type.this
            assert recvr.is_precise()
            typeinfer.add_type(self.value.name, recvr, loc=self.loc)
            source_constraint = typeinfer.refine_map.get(self.value.name)
            if source_constraint is not None:
                source_constraint.refine(typeinfer, recvr)

    def __repr__(self):
        return 'resolving type of attribute "{attr}" of "{value}"'.format(
            value=self.value, attr=self.attr)


class SetItemConstraint(object):
    def __init__(self, target, index, value, loc):
        self.target = target
        self.index = index
        self.value = value
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of setitem at {0}", self.loc):
            typevars = typeinfer.typevars
            if not all(typevars[var.name].defined
                       for var in (self.target, self.index, self.value)):
                return
            targetty = typevars[self.target.name].getone()
            idxty = typevars[self.index.name].getone()
            valty = typevars[self.value.name].getone()

            sig = typeinfer.context.resolve_setitem(targetty, idxty, valty)
            if sig is None:
                raise TypingError("Cannot resolve setitem: %s[%s] = %s" %
                                  (targetty, idxty, valty), loc=self.loc)

            # For array setitem, refine imprecise array dtype
            if _is_array_not_precise(targetty):
                assert sig.args[0].is_precise()
                typeinfer.add_type(self.target.name, sig.args[0], loc=self.loc)

            self.signature = sig

    def get_call_signature(self):
        return self.signature


class StaticSetItemConstraint(object):
    def __init__(self, target, index, index_var, value, loc):
        self.target = target
        self.index = index
        self.index_var = index_var
        self.value = value
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of staticsetitem at {0}", self.loc):
            typevars = typeinfer.typevars
            if not all(typevars[var.name].defined
                       for var in (self.target, self.index_var, self.value)):
                return
            targetty = typevars[self.target.name].getone()
            idxty = typevars[self.index_var.name].getone()
            valty = typevars[self.value.name].getone()

            sig = typeinfer.context.resolve_static_setitem(targetty,
                                                           self.index, valty)
            if sig is None:
                sig = typeinfer.context.resolve_setitem(targetty, idxty, valty)
            if sig is None:
                raise TypingError("Cannot resolve setitem: %s[%r] = %s" %
                                  (targetty, self.index, valty), loc=self.loc)
            self.signature = sig

    def get_call_signature(self):
        return self.signature


class DelItemConstraint(object):
    def __init__(self, target, index, loc):
        self.target = target
        self.index = index
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of delitem at {0}", self.loc):
            typevars = typeinfer.typevars
            if not all(typevars[var.name].defined
                       for var in (self.target, self.index)):
                return
            targetty = typevars[self.target.name].getone()
            idxty = typevars[self.index.name].getone()

            sig = typeinfer.context.resolve_delitem(targetty, idxty)
            if sig is None:
                raise TypingError("Cannot resolve delitem: %s[%s]" %
                                  (targetty, idxty), loc=self.loc)
            self.signature = sig

    def get_call_signature(self):
        return self.signature


class SetAttrConstraint(object):
    def __init__(self, target, attr, value, loc):
        self.target = target
        self.attr = attr
        self.value = value
        self.loc = loc

    def __call__(self, typeinfer):
        with new_error_context("typing of set attribute {0!r} at {1}",
                               self.attr, self.loc):
            typevars = typeinfer.typevars
            if not all(typevars[var.name].defined
                       for var in (self.target, self.value)):
                return
            targetty = typevars[self.target.name].getone()
            valty = typevars[self.value.name].getone()
            sig = typeinfer.context.resolve_setattr(targetty, self.attr,
                                                    valty)
            if sig is None:
                raise TypingError("Cannot resolve setattr: (%s).%s = %s" %
                                  (targetty, self.attr, valty),
                                  loc=self.loc)
            self.signature = sig

    def get_call_signature(self):
        return self.signature


class PrintConstraint(object):
    def __init__(self, args, vararg, loc):
        self.args = args
        self.vararg = vararg
        self.loc = loc

    def __call__(self, typeinfer):
        typevars = typeinfer.typevars

        r = fold_arg_vars(typevars, self.args, self.vararg, {})
        if r is None:
            # Cannot resolve call type until all argument types are known
            return
        pos_args, kw_args = r

        fnty = typeinfer.context.resolve_value_type(print)
        assert fnty is not None
        sig = typeinfer.resolve_call(fnty, pos_args, kw_args)
        self.signature = sig

    def get_call_signature(self):
        return self.signature


class TypeVarMap(dict):
    def set_context(self, context):
        self.context = context

    def __getitem__(self, name):
        if name not in self:
            self[name] = TypeVar(self.context, name)
        return super(TypeVarMap, self).__getitem__(name)

    def __setitem__(self, name, value):
        assert isinstance(name, str)
        if name in self:
            raise KeyError("Cannot redefine typevar %s" % name)
        else:
            super(TypeVarMap, self).__setitem__(name, value)


# A temporary mapping of {function name: dispatcher object}
_temporary_dispatcher_map = {}


@contextlib.contextmanager
def register_dispatcher(disp):
    """
    Register a Dispatcher for inference while it is not yet stored
    as global or closure variable (e.g. during execution of the @jit()
    call).  This allows resolution of recursive calls with eager
    compilation.
    """
    assert callable(disp)
    assert callable(disp.py_func)
    name = disp.py_func.__name__
    _temporary_dispatcher_map[name] = disp
    try:
        yield
    finally:
        del _temporary_dispatcher_map[name]


typeinfer_extensions = {}


class TypeInferer(object):
    """
    Operates on block that shares the same ir.Scope.
    """

    def __init__(self, context, func_ir, warnings):
        self.context = context
        # sort based on label, ensure iteration order!
        self.blocks = OrderedDict()
        for k in sorted(func_ir.blocks.keys()):
            self.blocks[k] = func_ir.blocks[k]
        self.generator_info = func_ir.generator_info
        self.func_id = func_ir.func_id
        self.func_ir = func_ir

        self.typevars = TypeVarMap()
        self.typevars.set_context(context)
        self.constraints = ConstraintNetwork()
        self.warnings = warnings

        # { index: mangled name }
        self.arg_names = {}
        # self.return_type = None
        # Set of assumed immutable globals
        self.assumed_immutables = set()
        # Track all calls and associated constraints
        self.calls = []
        # The inference result of the above calls
        self.calltypes = utils.UniqueDict()
        # Target var -> constraint with refine hook
        self.refine_map = {}

        if config.DEBUG or config.DEBUG_TYPEINFER:
            self.debug = TypeInferDebug(self)
        else:
            self.debug = NullDebug()

        self._skip_recursion = False

    def copy(self, skip_recursion=False):
        clone = TypeInferer(self.context, self.func_ir, self.warnings)
        clone.arg_names = self.arg_names.copy()
        clone._skip_recursion = skip_recursion

        for k, v in self.typevars.items():
            if not v.locked and v.defined:
                clone.typevars[k].add_type(v.getone(), loc=v.define_loc)

        return clone

    def _mangle_arg_name(self, name):
        # Disambiguise argument name
        return "arg.%s" % (name,)

    def _get_return_vars(self):
        rets = []
        for blk in utils.itervalues(self.blocks):
            inst = blk.terminator
            if isinstance(inst, ir.Return):
                rets.append(inst.value)
        return rets

    def seed_argument(self, name, index, typ):
        name = self._mangle_arg_name(name)
        self.seed_type(name, typ)
        self.arg_names[index] = name

    def seed_type(self, name, typ):
        """All arguments should be seeded.
        """
        self.lock_type(name, typ, loc=None)

    def seed_return(self, typ):
        """Seeding of return value is optional.
        """
        for var in self._get_return_vars():
            self.lock_type(var.name, typ, loc=None)

    def build_constraint(self):
        for blk in utils.itervalues(self.blocks):
            for inst in blk.body:
                self.constrain_statement(inst)

    def return_types_from_partial(self):
        """
        Resume type inference partially to deduce the return type.
        Note: No side-effect to `self`.

        Returns the inferred return type or None if it cannot deduce the return
        type.
        """
        # Clone the typeinferer and disable typing recursive calls
        cloned = self.copy(skip_recursion=True)
        # rebuild constraint network
        cloned.build_constraint()
        # propagate without raising
        cloned.propagate(raise_errors=False)
        # get return types
        rettypes = set()
        for retvar in cloned._get_return_vars():
            if retvar.name in cloned.typevars:
                typevar = cloned.typevars[retvar.name]
                if typevar and typevar.defined:
                    rettypes.add(types.unliteral(typevar.getone()))
        if not rettypes:
            return
        # unify return types
        return cloned._unify_return_types(rettypes)

    def propagate(self, raise_errors=True):
        newtoken = self.get_state_token()
        oldtoken = None
        # Since the number of types are finite, the typesets will eventually
        # stop growing.

        while newtoken != oldtoken:
            self.debug.propagate_started()
            oldtoken = newtoken
            # Errors can appear when the type set is incomplete; only
            # raise them when there is no progress anymore.
            errors = self.constraints.propagate(self)
            newtoken = self.get_state_token()
            self.debug.propagate_finished()
        if errors:
            if raise_errors:
                raise errors[0]
            else:
                return errors

    def add_type(self, var, tp, loc, unless_locked=False):
        assert isinstance(var, str), type(var)
        tv = self.typevars[var]
        if unless_locked and tv.locked:
            return
        oldty = tv.type
        unified = tv.add_type(tp, loc=loc)
        if unified != oldty:
            self.propagate_refined_type(var, unified)

    def add_calltype(self, inst, signature):
        assert signature is not None
        self.calltypes[inst] = signature

    def copy_type(self, src_var, dest_var, loc):
        self.typevars[dest_var].union(self.typevars[src_var], loc=loc)

    def lock_type(self, var, tp, loc, literal_value=NOTSET):
        tv = self.typevars[var]
        tv.lock(tp, loc=loc, literal_value=literal_value)

    def propagate_refined_type(self, updated_var, updated_type):
        source_constraint = self.refine_map.get(updated_var)
        if source_constraint is not None:
            source_constraint.refine(self, updated_type)

    def unify(self):
        """
        Run the final unification pass over all inferred types, and
        catch imprecise types.
        """
        typdict = utils.UniqueDict()

        def find_offender(name, exhaustive=False):
            # finds the offending variable definition by name
            # if exhaustive is set it will try and trace through temporary
            # variables to find a concrete offending definition.
            offender = None
            for block in self.func_ir.blocks.values():
                offender = block.find_variable_assignment(name)
                if offender is not None:
                    if not exhaustive:
                        break
                    try: # simple assignment
                        hasattr(offender.value, 'name')
                        offender_value = offender.value.name
                    except (AttributeError, KeyError):
                        break
                    orig_offender = offender
                    if offender_value.startswith('$'):
                        offender = find_offender(offender_value,
                                                 exhaustive=exhaustive)
                        if offender is None:
                            offender = orig_offender
                    break
            return offender

        def diagnose_imprecision(offender):
            # helper for diagnosing imprecise types

            list_msg = """\n
For Numba to be able to compile a list, the list must have a known and
precise type that can be inferred from the other variables. Whilst sometimes
the type of empty lists can be inferred, this is not always the case, see this
documentation for help:

http://numba.pydata.org/numba-doc/latest/user/troubleshoot.html#my-code-has-an-untyped-list-problem
"""
            if offender is not None:
                # This block deals with imprecise lists
                if hasattr(offender, 'value'):
                    if hasattr(offender.value, 'op'):
                        # might be `foo = []`
                        if offender.value.op == 'build_list':
                            return list_msg
                        # or might be `foo = list()`
                        elif offender.value.op == 'call':
                            try: # assignment involving a call
                                call_name = offender.value.func.name
                                # find the offender based on the call name
                                offender = find_offender(call_name)
                                if isinstance(offender.value, ir.Global):
                                    if offender.value.name == 'list':
                                        return list_msg
                            except (AttributeError, KeyError):
                                pass
            return "" # no help possible

        def check_var(name):
            tv = self.typevars[name]
            if not tv.defined:
                offender = find_offender(name)
                val = getattr(offender, 'value', 'unknown operation')
                loc = getattr(offender, 'loc', 'unknown location')
                msg = "Undefined variable '%s', operation: %s, location: %s"
                raise TypingError(msg % (var, val, loc), loc)
            tp = tv.getone()
            if not tp.is_precise():
                offender = find_offender(name, exhaustive=True)
                msg = ("Cannot infer the type of variable '%s'%s, "
                      "have imprecise type: %s. %s")
                istmp = " (temporary variable)" if var.startswith('$') else ""
                loc = getattr(offender, 'loc', 'unknown location')
                # is this an untyped list? try and provide help
                extra_msg = diagnose_imprecision(offender)
                raise TypingError(msg % (var, istmp, tp, extra_msg), loc)
            else: # type is precise, hold it
                typdict[var] = tp

        # For better error display, check first user-visible vars, then
        # temporaries
        temps = set(k for k in self.typevars if not k[0].isalpha())
        others = set(self.typevars) - temps
        for var in sorted(others):
            check_var(var)
        for var in sorted(temps):
            check_var(var)

        retty = self.get_return_type(typdict)
        fntys = self.get_function_types(typdict)
        if self.generator_info:
            retty = self.get_generator_type(typdict, retty)

        self.debug.unify_finished(typdict, retty, fntys)

        return typdict, retty, fntys

    def get_generator_type(self, typdict, retty):
        gi = self.generator_info
        arg_types = [None] * len(self.arg_names)
        for index, name in self.arg_names.items():
            arg_types[index] = typdict[name]
        state_types = [typdict[var_name] for var_name in gi.state_vars]
        yield_types = [typdict[y.inst.value.name]
                       for y in gi.get_yield_points()]
        if not yield_types:
            msg = "Cannot type generator: it does not yield any value"
            raise TypingError(msg)
        yield_type = self.context.unify_types(*yield_types)
        if yield_type is None:
            msg = "Cannot type generator: cannot unify yielded types %s"
            raise TypingError(msg % (yield_types,))
        return types.Generator(self.func_id.func, yield_type, arg_types,
                               state_types, has_finalizer=True)

    def get_function_types(self, typemap):
        """
        Fill and return the calltypes map.
        """
        # XXX why can't this be done on the fly?
        calltypes = self.calltypes
        for call, constraint in self.calls:
            calltypes[call] = constraint.get_call_signature()
        return calltypes

    def _unify_return_types(self, rettypes):
        if rettypes:
            unified = self.context.unify_types(*rettypes)
            if unified is None or not unified.is_precise():
                def check_type(atype):
                    lst = []
                    for k, v in self.typevars.items():
                        if atype == v.type:
                            lst.append(k)
                    returns = {}
                    for x in reversed(lst):
                        for block in self.func_ir.blocks.values():
                            for instr in block.find_insts(ir.Return):
                                value = instr.value
                                if isinstance(value, ir.Var):
                                    name = value.name
                                else:
                                    pass
                                if x == name:
                                    returns[x] = instr
                                    break

                    for name, offender in returns.items():
                        loc = getattr(offender, 'loc', 'unknown location')
                        msg = ("Return of: IR name '%s', type '%s', "
                               "location: %s")
                        interped = msg % (name, atype, loc.strformat())
                    return interped

                problem_str = []
                for xtype in rettypes:
                    problem_str.append(_termcolor.errmsg(check_type(xtype)))

                raise TypingError("Can't unify return type from the "
                                  "following types: %s"
                                  % ", ".join(sorted(map(str, rettypes))) +
                                  "\n" + "\n".join(problem_str))
            return unified
        else:
            # Function without a successful return path
            return types.none

    def get_return_type(self, typemap):
        rettypes = set()
        for var in self._get_return_vars():
            rettypes.add(typemap[var.name])
        return self._unify_return_types(rettypes)

    def get_state_token(self):
        """The algorithm is monotonic.  It can only grow or "refine" the
        typevar map.
        """
        return [tv.type for name, tv in sorted(self.typevars.items())]

    def constrain_statement(self, inst):
        if isinstance(inst, ir.Assign):
            self.typeof_assign(inst)
        elif isinstance(inst, ir.SetItem):
            self.typeof_setitem(inst)
        elif isinstance(inst, ir.StaticSetItem):
            self.typeof_static_setitem(inst)
        elif isinstance(inst, ir.DelItem):
            self.typeof_delitem(inst)
        elif isinstance(inst, ir.SetAttr):
            self.typeof_setattr(inst)
        elif isinstance(inst, ir.Print):
            self.typeof_print(inst)
        elif isinstance(inst, (ir.Jump, ir.Branch, ir.Return, ir.Del)):
            pass
        elif isinstance(inst, ir.StaticRaise):
            pass
        elif type(inst) in typeinfer_extensions:
            # let external calls handle stmt if type matches
            f = typeinfer_extensions[type(inst)]
            f(inst, self)
        else:
            msg = "Unsupported constraint encountered: %s" % inst
            raise UnsupportedError(msg, loc=inst.loc)

    def typeof_setitem(self, inst):
        constraint = SetItemConstraint(target=inst.target, index=inst.index,
                                       value=inst.value, loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst, constraint))

    def typeof_static_setitem(self, inst):
        constraint = StaticSetItemConstraint(target=inst.target,
                                             index=inst.index,
                                             index_var=inst.index_var,
                                             value=inst.value, loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst, constraint))

    def typeof_delitem(self, inst):
        constraint = DelItemConstraint(target=inst.target, index=inst.index,
                                       loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst, constraint))

    def typeof_setattr(self, inst):
        constraint = SetAttrConstraint(target=inst.target, attr=inst.attr,
                                       value=inst.value, loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst, constraint))

    def typeof_print(self, inst):
        constraint = PrintConstraint(args=inst.args, vararg=inst.vararg,
                                     loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst, constraint))

    def typeof_assign(self, inst):
        value = inst.value
        if isinstance(value, ir.Const):
            self.typeof_const(inst, inst.target, value.value)
        elif isinstance(value, ir.Var):
            self.constraints.append(Propagate(dst=inst.target.name,
                                              src=value.name, loc=inst.loc))
        elif isinstance(value, (ir.Global, ir.FreeVar)):
            self.typeof_global(inst, inst.target, value)
        elif isinstance(value, ir.Arg):
            self.typeof_arg(inst, inst.target, value)
        elif isinstance(value, ir.Expr):
            self.typeof_expr(inst, inst.target, value)
        elif isinstance(value, ir.Yield):
            self.typeof_yield(inst, inst.target, value)
        else:
            msg = ("Unsupported assignment encountered: %s %s" %
                   (type(value), str(value)))
            raise UnsupportedError(msg, loc=inst.loc)

    def resolve_value_type(self, inst, val):
        """
        Resolve the type of a simple Python value, such as can be
        represented by literals.
        """
        try:
            return self.context.resolve_value_type(val)
        except ValueError as e:
            msg = str(e)
        raise TypingError(msg, loc=inst.loc)

    def typeof_arg(self, inst, target, arg):
        src_name = self._mangle_arg_name(arg.name)
        self.constraints.append(ArgConstraint(dst=target.name,
                                              src=src_name,
                                              loc=inst.loc))

    def typeof_const(self, inst, target, const):
        ty = self.resolve_value_type(inst, const)
        if inst.value.use_literal_type:
            lit = types.maybe_literal(value=const)
        else:
            lit = None
        self.add_type(target.name, lit or ty, loc=inst.loc)

    def typeof_yield(self, inst, target, yield_):
        # Sending values into generators isn't supported.
        self.add_type(target.name, types.none, loc=inst.loc)

    def sentry_modified_builtin(self, inst, gvar):
        """
        Ensure that builtins are not modified.
        """
        if (gvar.name in ('range', 'xrange') and
                gvar.value not in utils.RANGE_ITER_OBJECTS):
            bad = True
        elif gvar.name == 'slice' and gvar.value is not slice:
            bad = True
        elif gvar.name == 'len' and gvar.value is not len:
            bad = True
        else:
            bad = False

        if bad:
            raise TypingError("Modified builtin '%s'" % gvar.name,
                              loc=inst.loc)

    def resolve_call(self, fnty, pos_args, kw_args):
        """
        Resolve a call to a given function type.  A signature is returned.
        """
        if isinstance(fnty, types.RecursiveCall) and not self._skip_recursion:
            # Recursive call
            disp = fnty.dispatcher_type.dispatcher
            pysig, args = disp.fold_argument_types(pos_args, kw_args)

            frame = self.context.callstack.match(disp.py_func, args)

            # If the signature is not being compiled
            if frame is None:
                sig = self.context.resolve_function_type(fnty.dispatcher_type,
                                                         pos_args, kw_args)
                fndesc = disp.overloads[args].fndesc
                fnty.overloads[args] = qualifying_prefix(fndesc.modname,
                                                         fndesc.unique_name)
                return sig

            fnid = frame.func_id
            fnty.overloads[args] = qualifying_prefix(fnid.modname,
                                                     fnid.unique_name)
            # Resume propagation in parent frame
            return_type = frame.typeinfer.return_types_from_partial()
            # No known return type
            if return_type is None:
                raise TypingError("cannot type infer runaway recursion")

            sig = typing.signature(return_type, *args)
            sig.pysig = pysig
            return sig
        else:
            # Normal non-recursive call
            return self.context.resolve_function_type(fnty, pos_args, kw_args)

    def typeof_global(self, inst, target, gvar):
        try:
            typ = self.resolve_value_type(inst, gvar.value)
        except TypingError as e:
            if (gvar.name == self.func_id.func_name
                    and gvar.name in _temporary_dispatcher_map):
                # Self-recursion case where the dispatcher is not (yet?) known
                # as a global variable
                typ = types.Dispatcher(_temporary_dispatcher_map[gvar.name])
            else:
                msg = _termcolor.errmsg("Untyped global name '%s':") + " %s"
                e.patch_message(msg % (gvar.name, e))
                raise

        if isinstance(typ, types.Dispatcher) and typ.dispatcher.is_compiling:
            # Recursive call
            callstack = self.context.callstack
            callframe = callstack.findfirst(typ.dispatcher.py_func)
            if callframe is not None:
                typ = types.RecursiveCall(typ)
            else:
                raise NotImplementedError(
                    "call to %s: unsupported recursion"
                    % typ.dispatcher)

        if isinstance(typ, types.Array):
            # Global array in nopython mode is constant
            typ = typ.copy(readonly=True)

        self.sentry_modified_builtin(inst, gvar)
        # Setting literal_value for globals because they are handled
        # like const value in numba
        lit = types.maybe_literal(gvar.value)
        self.lock_type(target.name, lit or typ, loc=inst.loc)
        self.assumed_immutables.add(inst)

    def typeof_expr(self, inst, target, expr):
        if expr.op == 'call':
            if isinstance(expr.func, ir.Intrinsic):
                sig = expr.func.type
                self.add_type(target.name, sig.return_type, loc=inst.loc)
                self.add_calltype(expr, sig)
            else:
                self.typeof_call(inst, target, expr)
        elif expr.op in ('getiter', 'iternext'):
            self.typeof_intrinsic_call(inst, target, expr.op, expr.value)
        elif expr.op == 'exhaust_iter':
            constraint = ExhaustIterConstraint(target.name, count=expr.count,
                                               iterator=expr.value,
                                               loc=expr.loc)
            self.constraints.append(constraint)
        elif expr.op == 'pair_first':
            constraint = PairFirstConstraint(target.name, pair=expr.value,
                                             loc=expr.loc)
            self.constraints.append(constraint)
        elif expr.op == 'pair_second':
            constraint = PairSecondConstraint(target.name, pair=expr.value,
                                              loc=expr.loc)
            self.constraints.append(constraint)
        elif expr.op == 'binop':
            self.typeof_intrinsic_call(inst, target, expr.fn, expr.lhs,
                                       expr.rhs)
        elif expr.op == 'inplace_binop':
            self.typeof_intrinsic_call(inst, target, expr.fn,
                                       expr.lhs, expr.rhs)
        elif expr.op == 'unary':
            self.typeof_intrinsic_call(inst, target, expr.fn, expr.value)
        elif expr.op == 'static_getitem':
            constraint = StaticGetItemConstraint(target.name, value=expr.value,
                                                 index=expr.index,
                                                 index_var=expr.index_var,
                                                 loc=expr.loc)
            self.constraints.append(constraint)
            self.calls.append((inst.value, constraint))
        elif expr.op == 'getitem':
            self.typeof_intrinsic_call(
                inst, target, operator.getitem, expr.value, expr.index,
                )
        elif expr.op == 'getattr':
            constraint = GetAttrConstraint(target.name, attr=expr.attr,
                                           value=expr.value, loc=inst.loc,
                                           inst=inst)
            self.constraints.append(constraint)
        elif expr.op == 'build_tuple':
            constraint = BuildTupleConstraint(target.name, items=expr.items,
                                              loc=inst.loc)
            self.constraints.append(constraint)
        elif expr.op == 'build_list':
            constraint = BuildListConstraint(target.name, items=expr.items,
                                             loc=inst.loc)
            self.constraints.append(constraint)
        elif expr.op == 'build_set':
            constraint = BuildSetConstraint(target.name, items=expr.items,
                                            loc=inst.loc)
            self.constraints.append(constraint)
        elif expr.op == 'cast':
            self.constraints.append(Propagate(dst=target.name,
                                              src=expr.value.name,
                                              loc=inst.loc))
        elif expr.op == 'make_function':
            self.lock_type(target.name, types.MakeFunctionLiteral(expr),
                           loc=inst.loc, literal_value=expr)
        else:
            msg = "Unsupported op-code encountered: %s" % expr
            raise UnsupportedError(msg, loc=inst.loc)

    def typeof_call(self, inst, target, call):
        constraint = CallConstraint(target.name, call.func.name, call.args,
                                    call.kws, call.vararg, loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst.value, constraint))

    def typeof_intrinsic_call(self, inst, target, func, *args):
        constraint = IntrinsicCallConstraint(target.name, func, args,
                                             kws=(), vararg=None, loc=inst.loc)
        self.constraints.append(constraint)
        self.calls.append((inst.value, constraint))


class NullDebug(object):

    def propagate_started(self):
        pass

    def propagate_finished(self):
        pass

    def unify_finished(self, typdict, retty, fntys):
        pass


class TypeInferDebug(object):

    def __init__(self, typeinfer):
        self.typeinfer = typeinfer

    def _dump_state(self):
        print('---- type variables ----')
        pprint([v for k, v in sorted(self.typeinfer.typevars.items())])

    def propagate_started(self):
        print("propagate".center(80, '-'))

    def propagate_finished(self):
        self._dump_state()

    def unify_finished(self, typdict, retty, fntys):
        print("Variable types".center(80, "-"))
        pprint(typdict)
        print("Return type".center(80, "-"))
        pprint(retty)
        print("Call types".center(80, "-"))
        pprint(fntys)
