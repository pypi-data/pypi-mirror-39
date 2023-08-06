from setuptools import setup, find_packages

setup(name='neuropot',
      version='0.1.1',
      description='Python package to preprocess brain MRI images and carry out population transfer and transfer learning',
      url='https://github.com/MEDCOMP/neuropot',
      author='Abhinit Ambastha',
      author_email='abhinit@comp.nus.edu.sg',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)