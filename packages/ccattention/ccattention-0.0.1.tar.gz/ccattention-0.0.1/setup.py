import setuptools

setuptools.setup(
    name='ccattention',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['_ext/__ext.so']},
)

