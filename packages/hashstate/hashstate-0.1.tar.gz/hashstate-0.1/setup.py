from setuptools import Extension, setup, find_packages

c_ext = Extension(
    'hashstate._hashstate',
    sources=['hashstate/_hashstate.c'],
    libraries=['ssl']
)

setup(
    name='hashstate',
    version='0.1',
    description='Serializable hash objects',
    packages=find_packages(),
    ext_modules=[c_ext]
)
