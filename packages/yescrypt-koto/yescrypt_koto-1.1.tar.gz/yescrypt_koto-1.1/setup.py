from setuptools import setup, Extension

yescrypt_module = Extension('yescrypt',
                            sources = ['yescrypt.c'],
                            extra_compile_args=['-O2', '-funroll-loops', '-fomit-frame-pointer'],
                            include_dirs=['.'])

setup (name = 'yescrypt_koto',
       version = '1.1',
       description = 'Bindings for yescrypt proof of work for Koto',
       long_description = 'Bindings for yescrypt proof of work for Koto',
       author = "WO",
       author_email = "wo@kotocoin.info",
       url='https://github.com/wo01/yescrypt_python/',
       install_requires=['cython'],
       ext_modules = [yescrypt_module])
