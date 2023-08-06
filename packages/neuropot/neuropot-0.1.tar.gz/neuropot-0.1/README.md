## NeuroPot: MRI preprocessing pipeline

Preprocessing pipeline:

- N4 normalization
- ACPC correction
- Skull stripping
- GM Segmentation
- Normalization
- Smoothing

```python
import os
from neuropot.preprocessing import n4_normalization, acpc_correction, skull_stripping, gm_segmentation, normalization, smoothing

path = os.getcwd()

# N4 normalization
image_N4_path = n4_normalization(path+"/input.nii")
print("Normalization done: ",image_N4_path)

# ACPC correction
image_N4_acpc_path = acpc_correction(image_N4_path)
print("ACPC correction done: ",image_N4_acpc_path)

# Skull stripping
image_N4_acpc_ss_path = skull_stripping(image_N4_acpc_path)
print("Skull stripping done: ",image_N4_acpc_ss_path)

# GM Segmentation
image_N4_acpc_ss_seg_path = gm_segmentation(image_N4_acpc_ss_path)
print("GM Segmentation done: ",image_N4_acpc_ss_seg_path)

# Normalization
image_N4_acpc_ss_seg_registered_path = normalization(image_N4_acpc_ss_seg_path)
print("Normalization done: ",image_N4_acpc_ss_seg_registered_path)

# Smoothing
image_N4_acpc_ss_seg_registered_smooth_path = smoothing(image_N4_acpc_ss_seg_registered_path)
print("Smoothing done: ",image_N4_acpc_ss_seg_registered_smooth_path)
```