from setuptools import setup, Extension

with open('README.md') as f:
    readme = f.read()

c_ext = Extension(
    'hashstate._hashstate',
    sources=['hashstate/_hashstate.c'],
    libraries=['ssl']
)

setup(
    name='hashstate',
    version='0.2.0',
    description='Serializable hash objects',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['hashstate'],
    ext_modules=[c_ext]
)
