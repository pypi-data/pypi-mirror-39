from setuptools import setup

setup(
    name='locuscomplexity',
    version='0.1.3dev0',
    packages = ['locuscomplexity'],
    url='https://github.com/LocusAnalytics/EconCmplx',
    long_description=open('README.md').read(),
    install_requires=[
          'pandas',],
    test_suite='nose.collector',
    tests_require=['nose'],
)