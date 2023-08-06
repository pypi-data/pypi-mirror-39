from setuptools import setup, find_packages

setup(name='neuropot',
      version='0.1.8',
      description='NeuroPot is a library which provides automated processing of neuroradiological images, data cleaning and manipulation functionality, machine learning algorithms and transfer learning methods.',
      url='https://github.com/MEDCOMP/neuropot',
      author='Abhinit Ambastha',
      author_email='abhinit@comp.nus.edu.sg',
      license='MIT',
      packages=find_packages(),
      package_data={
      	'neuropot.preprocessing':['template/*.nii']
      },
      scripts=[
      	'neuropot/preprocessing/bin/ACPCAlignment.sh'
      ],
      install_requires=[
      	'SimpleITK',
            'numpy'
      ],
      zip_safe=False)