from setuptools import setup

setup(
    name='locuscomplexity',
    version='0.1.4dev0',
    packages = ['locuscomplexity'],
    url='https://github.com/LocusAnalytics/EconCmplx',
    long_description=open('README.mst').read(),
    install_requires=[
          'pandas',],
    test_suite='nose.collector',
    tests_require=['nose'],
    data_files = [
        'data/dict_colors.pkl'
    ]
)