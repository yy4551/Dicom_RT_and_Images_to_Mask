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

create_path(example_path)
create_path(label_path)



for index,dcmfolder in enumerate(os.listdir(Dicom_path)):

    Dicom_reader = DicomReaderWriter(description='Examples', arg_max=True)
    fullpath = os.path.join(Dicom_path, dcmfolder)
    Dicom_reader.walk_through_folders(fullpath) # This will parse through all DICOM present in the folder and subfolders
    all_rois = Dicom_reader.return_rois(print_rois=True) # Return a list of all rois present

    Contour_names = all_rois # Define what rois you want
# associations = [ROIAssociationClass('tumor', ['tumor_mr', 'tumor_ct'])] # Any list of roi associations
    Dicom_reader.set_contour_names_and_associations(contour_names=Contour_names)


    Dicom_reader.get_images_and_mask()

    image_numpy = Dicom_reader.ArrayDicom
    mask_numpy = Dicom_reader.mask

    dicom_sitk_handle = Dicom_reader.dicom_handle # SimpleITK image handle
    mask_sitk_handle = Dicom_reader.annotation_handle

    padded_index = str(index + 1).zfill(3)
    logger.info(
        f'{dcmfolder.ljust(20)} = {padded_index.ljust(4)},depth={str(image_numpy.shape[0]).ljust(5)},  label = {str(Dicom_reader.all_rois).ljust(25)}, ')
    sitk.WriteImage(dicom_sitk_handle, os.path.join(example_path, f'volume_{padded_index}.nii.gz'))
    sitk.WriteImage(mask_sitk_handle, os.path.join(label_path, f'segmentation_{padded_index}.nii.gz'))