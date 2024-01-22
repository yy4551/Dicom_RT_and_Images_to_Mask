import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(r"C:\Users\admin\PycharmProjects\Dicom_RT_and_Images_to_Mask\log\log.txt")
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(module)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)