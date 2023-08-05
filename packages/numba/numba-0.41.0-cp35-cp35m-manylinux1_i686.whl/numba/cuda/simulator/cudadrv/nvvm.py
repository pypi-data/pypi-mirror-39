'''
NVVM is not supported in the simulator, but stubs are provided to allow tests
to import correctly.
'''

class NvvmSupportError(ImportError):
    pass

class NVVM(object):
    def __init__(self):
        raise NvvmSupportError('NVVM not supported in the simulator')

CompilationUnit = None
llvm_to_ptx = None
set_cuda_kernel = None
fix_data_layout = None
get_arch_option = None
SUPPORTED_CC = None
LibDevice = None
NvvmError = None

def is_available():
    return False
