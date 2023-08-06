from setuptools import setup, Extension

c_ext = Extension(
    'hashstate._hashstate',
    sources=['hashstate/_hashstate.c'],
    libraries=['ssl']
)

setup(
    name='hashstate',
    version='0.1.3',
    description='Serializable hash objects',
    packages=['hashstate'],
    ext_modules=[c_ext]
)
