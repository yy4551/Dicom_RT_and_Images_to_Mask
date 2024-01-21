import SimpleITK as sitk
import numpy as np

seg = sitk.ReadImage(r"C:\Git\DataSet\Pancreas\seg\seg_000.nii.gz")
a = sitk.GetArrayFromImage(seg)
pass
pass