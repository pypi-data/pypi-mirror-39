## NeuroPot

NeuroPot is a library which provides automated processing of neuroradiological images, data cleaning and manipulation functionality, machine learning algorithms and transfer learning methods.

### Quickstart

1. #### Setup FSL:

[Install FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation#Installing_FSL)
For MAC OSX, you can download the installer script [here](https://gist.github.com/abhinit/1cb51c695164497f068b608d3bad7565) 

It is important to follow the the [shell setup](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/ShellSetup), one way to check whether the shell is not configured is that all fsl applications will appear with a 'fsl-5.0' prefix e.g. 'fsl-5.0-bet' instead of 'bet'.

2. #### Install the neurpot package via pip:

```shell
pip install neuropot
```

3. #### Now you can import and use the processing pipeline as follows:

```python
import neuropot.preprocessing as preproc
```
or
```python
from neuropot.preprocessing import *
```
You can try the samples given below.

### Preprocessing pipeline:

This pipeline requires FSL: [Install FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation#Installing_FSL)

- N4 normalization
- ACPC correction
- Skull stripping
- GM Segmentation
- Normalization
- Smoothing

#### Preprocessing a single file:

```python
import os
import neuropot.preprocessing as preproc

path = os.getcwd()

# N4 normalization
# image_N4_path = preproc.n4_normalization(path+"/input.nii")
# print("Normalization done: ",image_N4_path)

# ACPC correction
image_N4_acpc_path = preproc.acpc_correction(path+"/input.nii")
print("ACPC correction done: ",image_N4_acpc_path)

# Skull stripping
image_N4_acpc_ss_path = preproc.skull_stripping(image_N4_acpc_path)
print("Skull stripping done: ",image_N4_acpc_ss_path)

# GM Segmentation
image_N4_acpc_ss_seg_path = preproc.gm_segmentation(image_N4_acpc_ss_path)
print("GM Segmentation done: ",image_N4_acpc_ss_seg_path)

# Normalization
image_N4_acpc_ss_seg_registered_path = preproc.normalization(image_N4_acpc_ss_seg_path)
print("Normalization done: ",image_N4_acpc_ss_seg_registered_path)

# Smoothing
image_N4_acpc_ss_seg_registered_smooth_path = preproc.smoothing(image_N4_acpc_ss_seg_registered_path)
print("Smoothing done: ",image_N4_acpc_ss_seg_registered_smooth_path)
```


#### Preprocessing multiple files:

```python
import os
import neuropot.preprocessing as preproc
from shutil import *

def preprocess(data_dir):
	processed = []
	total = len([file for file in os.listdir(data_dir) if file.endswith(".nii")])

	for idx,file in enumerate(os.listdir(data_dir)):
		if file.endswith(".nii"):
			input_file = os.path.join(data_dir, file)
			print("[%d/%d] Processing %s ... "%(idx+1,total,file),end="", flush=True),
			image_N4_acpc_path = preproc.acpc_correction(input_file)
			image_N4_acpc_ss_path = preproc.skull_stripping(image_N4_acpc_path)
			image_N4_acpc_ss_seg_path = preproc.gm_segmentation(image_N4_acpc_ss_path)
			image_N4_acpc_ss_seg_registered_path = preproc.normalization(image_N4_acpc_ss_seg_path)
			image_N4_acpc_ss_seg_registered_smooth_path = preproc.smoothing(image_N4_acpc_ss_seg_registered_path)
			processed.append(image_N4_acpc_ss_seg_registered_smooth_path)

			copyfile(image_N4_acpc_ss_seg_registered_smooth_path, os.path.join(data_dir,'processed_'+file+'.gz'))
			
			print("[DONE]")

	return processed

def main():
	data_dir = os.path.abspath("./mri")
	processed_files = preprocess(data_dir)
	print(processed_files)

main()
```
