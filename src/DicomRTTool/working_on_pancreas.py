import shutil
from ReaderWriter import DicomReaderWriter
import SimpleITK as sitk
import os
from log import logger
import numpy as np


def create_path(path):
    if os.path.exists(path) is True:
        shutil.rmtree(path)
    os.mkdir(path)
    return path

Dicom_path = r'C:\Git\DataSet\Pancreas\None-Enhanced-156 Patients-169 CT'
img_path = r'C:\Git\MONAI_DATA_DIRECTORY\Task01_pancreas\img'
seg_path = r'C:\Git\MONAI_DATA_DIRECTORY\Task01_pancreas\seg'
pancreas_seg_path = r'C:\Git\MONAI_DATA_DIRECTORY\Task01_pancreas\pancreas_seg'
tumor_seg_path = r'C:\Git\MONAI_DATA_DIRECTORY\Task01_pancreas\tumor_seg'
ctv_seg_path = r'C:\Git\MONAI_DATA_DIRECTORY\Task01_pancreas\ctv_seg'

create_path(img_path)
create_path(seg_path)
create_path(pancreas_seg_path)
create_path(tumor_seg_path)
create_path(ctv_seg_path)


who_has_tiny_pancreas = []
no_pancreas = []
no_tumor = []
no_ctv = []

for _,dcmfolder in enumerate(os.listdir(Dicom_path)):
    Dicom_reader = DicomReaderWriter(description='Examples', arg_max=False)
    fullpath = os.path.join(Dicom_path, dcmfolder)
    Dicom_reader.walk_through_folders(fullpath) # This will parse through all DICOM present in the folder and subfolders
    all_rois = Dicom_reader.return_rois(print_rois=True)
    if 'pancreas' not in all_rois:
        no_pancreas.append(dcmfolder)
    if 'tumor' not in all_rois:
        no_tumor.append(dcmfolder)
    if 'ctv' not in all_rois:
        no_ctv.append(dcmfolder)
        # Return a list of all rois present

    Contour_names = ['tumor', 'ctv', 'pancreas'] # Define what rois you want
# associations = [ROIAssociationClass('tumor', ['tumor_mr', 'tumor_ct'])] # Any list of roi associations
    Dicom_reader.set_contour_names_and_associations(contour_names=Contour_names)

    Dicom_reader.get_images_and_mask()

    tumor_numpy = Dicom_reader.mask[0]
    ctv_numpy = Dicom_reader.mask[1]
    pancreas_numpy = Dicom_reader.mask[2]

    tumor_size = np.count_nonzero(Dicom_reader.mask[0])
    ctv_size = np.count_nonzero(Dicom_reader.mask[1])
    pancreas_size = np.count_nonzero(Dicom_reader.mask[2])

    if tumor_size > pancreas_size or ctv_size > pancreas_size:
        who_has_tiny_pancreas.append(dcmfolder)

    logger.info(f'{dcmfolder} : img_shape = {Dicom_reader.ArrayDicom.shape}, seg_shape = {Dicom_reader.mask.shape}'
                f' tumor_size = {tumor_size},ctv_size = {ctv_size},pancreas_size = {pancreas_size}')

    sitk.WriteImage(Dicom_reader.dicom_handle, os.path.join(img_path, f'img_{dcmfolder}.nii.gz'))
    sitk.WriteImage(Dicom_reader.annotation_handle, os.path.join(seg_path, f'seg_{dcmfolder}.nii.gz'))
    sitk.WriteImage(sitk.GetImageFromArray(pancreas_numpy), os.path.join(pancreas_seg_path, f'pancreas_seg_{dcmfolder}.nii.gz'))
    sitk.WriteImage(sitk.GetImageFromArray(tumor_numpy), os.path.join(tumor_seg_path, f'tumor_seg_{dcmfolder}.nii.gz'))
    sitk.WriteImage(sitk.GetImageFromArray(ctv_numpy), os.path.join(ctv_seg_path, f'ctv_seg_{dcmfolder}.nii.gz'))

logger.info(f"no_pancreas = {no_pancreas}")
logger.info(f"mo_tumor = {no_tumor}")
logger.info(f"no_ctv = {no_ctv}")
logger.info(f"who_has_tiny_pancreas={who_has_tiny_pancreas}")
