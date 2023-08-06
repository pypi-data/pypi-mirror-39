from setuptools import setup, find_packages

setup(name='neuropot',
      version='0.1.2',
      description='NeuroPot is a library which provides automated processing of neuroradiological images, data cleaning and manipulation functionality, machine learning algorithms and transfer learning methods.',
      url='https://github.com/MEDCOMP/neuropot',
      author='Abhinit Ambastha',
      author_email='abhinit@comp.nus.edu.sg',
      license='MIT',
      packages=find_packages(),
      install_requires=[
      	'SimpleITK'
      ],
      zip_safe=False)