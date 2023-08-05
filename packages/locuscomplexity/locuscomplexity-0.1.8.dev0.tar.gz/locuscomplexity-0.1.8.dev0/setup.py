from setuptools import setup

setup(
    name='locuscomplexity',
    version='0.1.8dev0',
    packages = ['locuscomplexity'],
    url='https://github.com/LocusAnalytics/EconCmplx',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
          'pandas','networkx', 'matplotlib'],
    test_suite='nose.collector',
    tests_require=['nose'],
    data_files = [
        ('data','data/dict_colors.pkl')
    ]
)