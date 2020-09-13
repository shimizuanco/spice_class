import spiceypy as spice
from spiceypy.utils.exceptions import SpiceyError
import os.path
import logging


class Sc:
    def __init__(self, meta_kernel_path):
        self.meta_kernel_path = meta_kernel_path
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unload()
        pass

    def invoke(self):
        self.logger.debug('invoke __name__:' + __name__)
        return True

    def load(self):
        # Change current directory to it where the meta-kernel file exists.
        try:
            kernel_dir = os.path.dirname(self.meta_kernel_path)
            os.chdir(os.path.expanduser(kernel_dir))
        except:
            self.logger.info('It could not find or load the meta-kernel file at', self.meta_kernel_path, '.')
            raise
        # Load the kernel file(s).
        try:
            spice.furnsh(self.meta_kernel_path)
        except SpiceyError:
            self.logger.info('Could not load the kernel(s) in the file', self.meta_kernel_path)
            raise

        self.logger.info('complete to load kernels.')

    def unload(self):
        spice.kclear()
        self.logger.info('Kernels of class ' + str(self) + ' are cleared.')
