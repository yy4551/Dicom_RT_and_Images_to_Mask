import nibabel as nib
import shutil
from ReaderWriter import DicomReaderWriter
import SimpleITK as sitk
import os
from log import logger


def create_path(path):
    if os.path.exists(path) is True:
        shutil.rmtree(path)
    os.mkdir(path)
    return path


Dicom_path = r'C:\Git\DataSet\Pancreas\None-Enhanced-156 Patients-169 CT'
example_path = r'C:\Git\DataSet\Pancreas\volume'
label_path = r'C:\Git\DataSet\Pancreas\segmentation'

compressed_volume_path = r'C:\Git\DataSet\Pancreas\compressed_volume'
compressed_label_path = r'C:\Git\DataSet\Pancreas\compressed_segmentation'

create_path(compressed_label_path)

for nii in os.listdir(label_path):
    img = nib.load(os.path.join(label_path, nii))
    nib.save(img, os.path.join(compressed_label_path, nii.replace('.nii', '.nii.gz')))
