from setuptools import setup, find_packages


setup(name='AIops tools',
      version='0.0.0',
      description='Tools for AIops.',
      author='Xinpu Ji',
      author_email='jixinpu@126.com',
      install_requires=[
          'pybrain', 'pandas', 'sklearn', 'statsmodels', 'numpy', 'tensorflow', 'dtw', 'matplotlib'],
      packages=find_packages(),
      keywords=[
          'AIops',
          'machine learning',
      ])
