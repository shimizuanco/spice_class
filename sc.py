import spiceypy as spice
from spiceypy.utils.exceptions import SpiceyError
import os.path
import logging


class Sc:
    __count = {}

    def __init__(self, meta_kernel_path):
        self.meta_kernel_path = meta_kernel_path
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.load_kernels()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unload_kernels()
        pass

    def invoke(self):
        self.logger.info('invoke __name__ is ' + __name__)
        return True

    def load_kernels(self):
        if not self.is_kernel_already_loaded():
            # Load the kernel file(s).
            self.furnish_kernels()
            # logging the kernel names after loading.
            self.logging_kernel_names()
        self.add_count()

    def is_kernel_already_loaded(self):
        result = False
        n_kernels = spice.ktotal('ALL')
        for i in range(n_kernels):
            file, _, source, _ = spice.kdata(i, 'ALL')
            if file == self.meta_kernel_path:
                msg = 'Already loaded. file: {:s}, source: {:s}.'.format(file, source)
                result = True
                break
        return result

    def furnish_kernels(self):
        # Change current directory to it where the meta-kernel file exists.
        kernel_dir = ''
        try:
            kernel_dir = os.path.dirname(self.meta_kernel_path)
            os.chdir(os.path.expanduser(kernel_dir))
        except Exception as e:
            msg = '{:s} Could not find the directory of {:s}.'.format(str(type(e)), kernel_dir)
            self.logger.error(msg)
            raise

        # furnish the kernel file(s).
        try:
            spice.furnsh(self.meta_kernel_path)
        except Exception as e:
            msg = '{:s} Failed to load the kernel(s) in the file {:s}.'.format(str(type(e)), self.meta_kernel_path)
            self.logger.error(msg)
            raise
        else:
            msg = 'Complete to load kernels from {:s}.'.format(self.meta_kernel_path)
            self.logger.info(msg)

    def logging_kernel_names(self):
        n_kernels = spice.ktotal('ALL')
        msg = 'After loading/unloading kernels in {:s}, {:d} kernel files are loaded.'.format(
            self.meta_kernel_path,
            n_kernels)
        self.logger.info(msg)
        for i in range(n_kernels):
            self.logger.debug(spice.kdata(i, 'ALL'))

    def unload_kernels(self):
        self.sub_count()
        if self.get_count() <= 0:
            spice.unload(self.meta_kernel_path)
            msg = 'Kernels in the file {:s} are unloaded.'.format(self.meta_kernel_path)
            self.logger.info(msg)
            self.logging_kernel_names()
        else:
            msg = '{:s} is still used by {:d} objects.'.format(
                self.meta_kernel_path,
                self.get_count())
            self.logger.info(msg)

    def add_count(self):
        key = self.meta_kernel_path
        self.__class__.__count[key] = self.get_count() + 1

    def sub_count(self):
        key = self.meta_kernel_path
        self.__class__.__count[key] -= 1

    def get_count(self):
        key = self.meta_kernel_path
        return self.__class__.__count.get(key, 0)
