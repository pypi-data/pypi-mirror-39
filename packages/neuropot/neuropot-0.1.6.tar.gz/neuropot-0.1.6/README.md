## NeuroPot

NeuroPot is a library which provides automated processing of neuroradiological images, data cleaning and manipulation functionality, machine learning algorithms and transfer learning methods.

### Preprocessing pipeline:

This pipeline requires FSL: [Install FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation#Installing_FSL)

- N4 normalization
- ACPC correction
- Skull stripping
- GM Segmentation
- Normalization
- Smoothing

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
