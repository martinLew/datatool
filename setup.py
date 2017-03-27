from distutils.core import setup
from distutils.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        _build_py.run(self)
        self.copy_file(
            'gfunddataprocessor/logger.conf',
            'build/lib/gfunddataprocessor/logger.conf', preserve_mode=0)

setup(
    name='gfund',
    version='1.0.3',
    description='The first verion of gfund data processor',
    author='luyiming',
    author_email='luyiming@gfund.com',
    packages=['gfunddataprocessor'],
    cmdclass={'build_py': build_py})
