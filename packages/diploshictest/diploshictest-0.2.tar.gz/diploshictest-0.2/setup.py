from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='diploshictest',
      version='0.2',
      description='DiploS/HIC',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jgallowa07/diploSHIC',
      author='Andrew Kern',
      author_email='',
      license='MIT',      
      packages=find_packages(exclude=[]),
      install_requires=['numpy',
                        'scipy',
                        'pandas',
                        'scikit-allel',
                        'scikit-learn',
                        'tensorflow',
                        'keras'],
      scripts=['diploshic/diploSHIC'],
      zip_safe=False,
      extras_require={
          'dev': [],
      },
      setup_requires=[],
)

