from __future__ import print_function

import sys
import numpy as np

import numba.unittest_support as unittest
from numba.compiler import compile_isolated, Flags
from numba import jit, njit, types
from .support import TestCase, MemoryLeakMixin, tag
from numba import testing
from numba.datamodel.testing import test_factory


enable_pyobj_flags = Flags()
enable_pyobj_flags.set("enable_pyobject")

forceobj_flags = Flags()
forceobj_flags.set("force_pyobject")

no_pyobj_flags = Flags()


def make_consumer(gen_func):
    def consumer(x):
        res = 0.0
        for y in gen_func(x):
            res += y
        return res

    return consumer


def gen1(x):
    for i in range(x):
        yield i


def gen2(x):
    for i in range(x):
        yield i
        for j in range(1, 3):
            yield i + j


def gen3(x):
    # Polymorphic yield types must be unified
    yield x
    yield x + 1.5
    yield x + 1j


def gen4(x, y, z):
    for i in range(3):
        yield z
        yield y + z
    return
    yield x


def gen5():
    # The bytecode for this generator doesn't contain any YIELD_VALUE
    # (it's optimized away).  We fail typing it, since the yield type
    # is entirely undefined.
    if 0:
        yield 1


def gen6(a, b):
    # Infinite loop: exercise computation of state variables
    x = a + 1
    while True:
        y = b + 2
        yield x + y


def gen7(arr):
    # Array variable in generator state
    for i in range(arr.size):
        yield arr[i]


# Optional arguments and boolean state members
def gen8(x=1, y=2, b=False):
    bb = not b
    yield x
    if bb:
        yield y
    if b:
        yield x + y


def genobj(x):
    object()
    yield x


def return_generator_expr(x):
    return (i * 2 for i in x)


def gen_ndindex(shape):
    for ind in np.ndindex(shape):
        yield ind


def gen_flat(arr):
    for val in arr.flat:
        yield val


def gen_ndenumerate(arr):
    for tup in np.ndenumerate(arr):
        yield tup


def gen_bool():
    yield True

class TestGenerators(MemoryLeakMixin, TestCase):
    def check_generator(self, pygen, cgen):
        self.assertEqual(next(cgen), next(pygen))
        # Use list comprehensions to make sure we trash the generator's
        # former C stack.
        expected = [x for x in pygen]
        got = [x for x in cgen]
        self.assertEqual(expected, got)
        with self.assertRaises(StopIteration):
            next(cgen)

    def check_gen1(self, flags=no_pyobj_flags):
        pyfunc = gen1
        cr = compile_isolated(pyfunc, (types.int32,), flags=flags)
        pygen = pyfunc(8)
        cgen = cr.entry_point(8)
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen1(self):
        self.check_gen1()

    def test_gen1_objmode(self):
        self.check_gen1(flags=forceobj_flags)

    def check_gen2(self, flags=no_pyobj_flags):
        pyfunc = gen2
        cr = compile_isolated(pyfunc, (types.int32,), flags=flags)
        pygen = pyfunc(8)
        cgen = cr.entry_point(8)
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen2(self):
        self.check_gen2()

    def test_gen2_objmode(self):
        self.check_gen2(flags=forceobj_flags)

    def check_gen3(self, flags=no_pyobj_flags):
        pyfunc = gen3
        cr = compile_isolated(pyfunc, (types.int32,), flags=flags)
        pygen = pyfunc(8)
        cgen = cr.entry_point(8)
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen3(self):
        self.check_gen3()

    def test_gen3_objmode(self):
        self.check_gen3(flags=forceobj_flags)

    def check_gen4(self, flags=no_pyobj_flags):
        pyfunc = gen4
        cr = compile_isolated(pyfunc, (types.int32,) * 3, flags=flags)
        pygen = pyfunc(5, 6, 7)
        cgen = cr.entry_point(5, 6, 7)
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen4(self):
        self.check_gen4()

    def test_gen4_objmode(self):
        self.check_gen4(flags=forceobj_flags)

    def test_gen5(self):
        with self.assertTypingError() as cm:
            cr = compile_isolated(gen5, ())
        self.assertIn("Cannot type generator: it does not yield any value",
                      str(cm.exception))

    def test_gen5_objmode(self):
        cr = compile_isolated(gen5, (), flags=forceobj_flags)
        cgen = cr.entry_point()
        self.assertEqual(list(cgen), [])
        with self.assertRaises(StopIteration):
            next(cgen)

    def check_gen6(self, flags=no_pyobj_flags):
        pyfunc = gen6
        cr = compile_isolated(pyfunc, (types.int32,) * 2, flags=flags)
        cgen = cr.entry_point(5, 6)
        l = []
        for i in range(3):
            l.append(next(cgen))
        self.assertEqual(l, [14] * 3)

    @tag('important')
    def test_gen6(self):
        self.check_gen6()

    def test_gen6_objmode(self):
        self.check_gen6(flags=forceobj_flags)

    def check_gen7(self, flags=no_pyobj_flags):
        pyfunc = gen7
        cr = compile_isolated(pyfunc, (types.Array(types.float64, 1, 'C'),),
                              flags=flags)
        arr = np.linspace(1, 10, 7)
        pygen = pyfunc(arr.copy())
        cgen = cr.entry_point(arr)
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen7(self):
        self.check_gen7()

    def test_gen7_objmode(self):
        self.check_gen7(flags=forceobj_flags)

    def check_gen8(self, **jit_args):
        pyfunc = gen8
        cfunc = jit(**jit_args)(pyfunc)

        def check(*args, **kwargs):
            self.check_generator(pyfunc(*args, **kwargs),
                                 cfunc(*args, **kwargs))

        check(2, 3)
        check(4)
        check(y=5)
        check(x=6, b=True)

    @tag('important')
    def test_gen8(self):
        self.check_gen8(nopython=True)

    def test_gen8_objmode(self):
        self.check_gen8(forceobj=True)

    def check_gen9(self, flags=no_pyobj_flags):
        pyfunc = gen_bool
        cr = compile_isolated(pyfunc, (), flags=flags)
        pygen = pyfunc()
        cgen = cr.entry_point()
        self.check_generator(pygen, cgen)

    @tag('important')
    def test_gen9(self):
        self.check_gen9(flags=no_pyobj_flags)

    def test_gen9_objmode(self):
        self.check_gen9(flags=forceobj_flags)

    def check_consume_generator(self, gen_func):
        cgen = jit(nopython=True)(gen_func)
        cfunc = jit(nopython=True)(make_consumer(cgen))
        pyfunc = make_consumer(gen_func)
        expected = pyfunc(5)
        got = cfunc(5)
        self.assertPreciseEqual(got, expected)

    def test_consume_gen1(self):
        self.check_consume_generator(gen1)

    def test_consume_gen2(self):
        self.check_consume_generator(gen2)

    @tag('important')
    def test_consume_gen3(self):
        self.check_consume_generator(gen3)

    # Check generator storage of some types

    def check_ndindex(self, flags=no_pyobj_flags):
        pyfunc = gen_ndindex
        cr = compile_isolated(pyfunc, (types.UniTuple(types.intp, 2),),
                              flags=flags)
        shape = (2, 3)
        pygen = pyfunc(shape)
        cgen = cr.entry_point(shape)
        self.check_generator(pygen, cgen)

    def test_ndindex(self):
        self.check_ndindex()

    def test_ndindex_objmode(self):
        self.check_ndindex(flags=forceobj_flags)

    def check_np_flat(self, pyfunc, flags=no_pyobj_flags):
        cr = compile_isolated(pyfunc, (types.Array(types.int32, 2, "C"),),
                              flags=flags)
        arr = np.arange(6, dtype=np.int32).reshape((2, 3))
        self.check_generator(pyfunc(arr), cr.entry_point(arr))
        cr = compile_isolated(pyfunc, (types.Array(types.int32, 2, "A"),),
                              flags=flags)
        arr = arr.T
        self.check_generator(pyfunc(arr), cr.entry_point(arr))

    def test_np_flat(self):
        self.check_np_flat(gen_flat)

    def test_np_flat_objmode(self):
        self.check_np_flat(gen_flat, flags=forceobj_flags)

    def test_ndenumerate(self):
        self.check_np_flat(gen_ndenumerate)

    def test_ndenumerate_objmode(self):
        self.check_np_flat(gen_ndenumerate, flags=forceobj_flags)


class TestGenExprs(MemoryLeakMixin, TestCase):
    @testing.allow_interpreter_mode
    def test_return_generator_expr(self):
        pyfunc = return_generator_expr
        cr = compile_isolated(pyfunc, ())
        cfunc = cr.entry_point
        self.assertEqual(sum(cfunc([1, 2, 3])), sum(pyfunc([1, 2, 3])))


def nrt_gen0(ary):
    for elem in ary:
        yield elem


def nrt_gen1(ary1, ary2):
    for e1, e2 in zip(ary1, ary2):
        yield e1
        yield e2


class TestNrtArrayGen(MemoryLeakMixin, TestCase):
    def test_nrt_gen0(self):
        pygen = nrt_gen0
        cgen = jit(nopython=True)(pygen)

        py_ary = np.arange(10)
        c_ary = py_ary.copy()

        py_res = list(pygen(py_ary))
        c_res = list(cgen(c_ary))

        np.testing.assert_equal(py_ary, c_ary)
        self.assertEqual(py_res, c_res)
        # Check reference count
        self.assertEqual(sys.getrefcount(py_ary),
                         sys.getrefcount(c_ary))

    def test_nrt_gen1(self):
        pygen = nrt_gen1
        cgen = jit(nopython=True)(pygen)

        py_ary1 = np.arange(10)
        py_ary2 = py_ary1 + 100

        c_ary1 = py_ary1.copy()
        c_ary2 = py_ary2.copy()

        py_res = list(pygen(py_ary1, py_ary2))
        c_res = list(cgen(c_ary1, c_ary2))

        np.testing.assert_equal(py_ary1, c_ary1)
        np.testing.assert_equal(py_ary2, c_ary2)
        self.assertEqual(py_res, c_res)
        # Check reference count
        self.assertEqual(sys.getrefcount(py_ary1),
                         sys.getrefcount(c_ary1))
        self.assertEqual(sys.getrefcount(py_ary2),
                         sys.getrefcount(c_ary2))

    def test_combine_gen0_gen1(self):
        """
        Issue #1163 is observed when two generator with NRT object arguments
        is ran in sequence.  The first one does a invalid free and corrupts
        the NRT memory subsystem.  The second generator is likely to segfault
        due to corrupted NRT data structure (an invalid MemInfo).
        """
        self.test_nrt_gen0()
        self.test_nrt_gen1()

    def test_nrt_gen0_stop_iteration(self):
        """
        Test cleanup on StopIteration
        """
        pygen = nrt_gen0
        cgen = jit(nopython=True)(pygen)

        py_ary = np.arange(1)
        c_ary = py_ary.copy()

        py_iter = pygen(py_ary)
        c_iter = cgen(c_ary)

        py_res = next(py_iter)
        c_res = next(c_iter)

        with self.assertRaises(StopIteration):
            py_res = next(py_iter)

        with self.assertRaises(StopIteration):
            c_res = next(c_iter)

        del py_iter
        del c_iter

        np.testing.assert_equal(py_ary, c_ary)
        self.assertEqual(py_res, c_res)
        # Check reference count
        self.assertEqual(sys.getrefcount(py_ary),
                         sys.getrefcount(c_ary))

    def test_nrt_gen0_no_iter(self):
        """
        Test cleanup for a initialized but never iterated (never call next())
        generator.
        """
        pygen = nrt_gen0
        cgen = jit(nopython=True)(pygen)

        py_ary = np.arange(1)
        c_ary = py_ary.copy()

        py_iter = pygen(py_ary)
        c_iter = cgen(c_ary)

        del py_iter
        del c_iter

        np.testing.assert_equal(py_ary, c_ary)

        # Check reference count
        self.assertEqual(sys.getrefcount(py_ary),
                         sys.getrefcount(c_ary))


# TODO: fix nested generator and MemoryLeakMixin
class TestNrtNestedGen(TestCase):
    def test_nrt_nested_gen(self):

        def gen0(arr):
            for i in range(arr.size):
                yield arr

        def factory(gen0):
            def gen1(arr):
                out = np.zeros_like(arr)
                for x in gen0(arr):
                    out = out + x
                return out, arr

            return gen1

        py_arr = np.arange(10)
        c_arr = py_arr.copy()
        py_res, py_old = factory(gen0)(py_arr)
        c_gen = jit(nopython=True)(factory(jit(nopython=True)(gen0)))
        c_res, c_old = c_gen(c_arr)

        self.assertIsNot(py_arr, c_arr)
        self.assertIs(py_old, py_arr)
        self.assertIs(c_old, c_arr)

        np.testing.assert_equal(py_res, c_res)

        self.assertEqual(sys.getrefcount(py_res),
                         sys.getrefcount(c_res))

        # The below test will fail due to generator finalizer not invoked.
        # This kept a reference of the c_old.
        #
        # self.assertEqual(sys.getrefcount(py_old),
        #                  sys.getrefcount(c_old))

    @unittest.expectedFailure
    def test_nrt_nested_gen_refct(self):
        def gen0(arr):
            yield arr

        def factory(gen0):
            def gen1(arr):
                for out in gen0(arr):
                    return out

            return gen1

        py_arr = np.arange(10)
        c_arr = py_arr.copy()
        py_old = factory(gen0)(py_arr)
        c_gen = jit(nopython=True)(factory(jit(nopython=True)(gen0)))
        c_old = c_gen(c_arr)

        self.assertIsNot(py_arr, c_arr)
        self.assertIs(py_old, py_arr)
        self.assertIs(c_old, c_arr)

        self.assertEqual(sys.getrefcount(py_old),
                         sys.getrefcount(c_old))

    def test_nrt_nested_nopython_gen(self):
        """
        Test nesting three generators
        """

        def factory(decor=lambda x: x):
            @decor
            def foo(a, n):
                for i in range(n):
                    yield a[i]
                    a[i] += i

            @decor
            def bar(n):
                a = np.arange(n)
                for i in foo(a, n):
                    yield i * 2
                for i in range(a.size):
                    yield a[i]

            @decor
            def cat(n):
                for i in bar(n):
                    yield i + i

            return cat

        py_gen = factory()
        c_gen = factory(jit(nopython=True))

        py_res = list(py_gen(10))
        c_res = list(c_gen(10))

        self.assertEqual(py_res, c_res)


class TestGeneratorWithNRT(MemoryLeakMixin, TestCase):
    def test_issue_1254(self):
        """
        Missing environment for returning array
        """

        @jit(nopython=True)
        def random_directions(n):
            for i in range(n):
                vec = np.empty(3)
                vec[:] = 12
                yield vec

        outputs = list(random_directions(5))
        self.assertEqual(len(outputs), 5)

        expect = np.empty(3)
        expect[:] = 12
        for got in outputs:
            np.testing.assert_equal(expect, got)

    def test_issue_1265(self):
        """
        Double-free for locally allocated, non escaping NRT objects
        """

        def py_gen(rmin, rmax, nr):
            a = np.linspace(rmin, rmax, nr)
            yield a[0]
            yield a[1]

        c_gen = jit(nopython=True)(py_gen)

        py_res = list(py_gen(-2, 2, 100))
        c_res = list(c_gen(-2, 2, 100))

        self.assertEqual(py_res, c_res)

        def py_driver(args):
            rmin, rmax, nr = args
            points = np.empty(nr, dtype=np.complex128)
            for i, c in enumerate(py_gen(rmin, rmax, nr)):
                points[i] = c

            return points

        @jit(nopython=True)
        def c_driver(args):
            rmin, rmax, nr = args
            points = np.empty(nr, dtype=np.complex128)
            for i, c in enumerate(c_gen(rmin, rmax, nr)):
                points[i] = c

            return points

        n = 2
        patches = (-2, -1, n)

        py_res = py_driver(patches)
        # The error will cause a segfault here
        c_res = c_driver(patches)

        np.testing.assert_equal(py_res, c_res)

    def test_issue_1808(self):
        """
        Incorrect return data model
        """
        magic = 0xdeadbeef

        @njit
        def generator():
            yield magic

        @njit
        def get_generator():
            return generator()

        @njit
        def main():
            out = 0
            for x in get_generator():
                out += x

            return out

        self.assertEqual(main(), magic)


class TestGeneratorModel(test_factory()):
    fe_type = types.Generator(gen_func=None, yield_type=types.int32,
                              arg_types=[types.int64, types.float32],
                              state_types=[types.intp, types.intp[::1]],
                              has_finalizer=False)


if __name__ == '__main__':
    unittest.main()
