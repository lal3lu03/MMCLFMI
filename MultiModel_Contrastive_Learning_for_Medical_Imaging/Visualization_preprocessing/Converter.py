import os
import csv
import pydicom
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

class DicomToJpegConverter:
    def __init__(self, input_dir, output_dir, num_processes=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.num_processes = num_processes or cpu_count()
        self.num_corrupted_files = 0
        self.corrupted_files = []

    def convert(self):
        dicom_files = self._get_dicom_files()
        self._create_output_dir()

        with Pool(self.num_processes) as pool:
            with tqdm(total=len(dicom_files), desc='Converting DICOM to JPEG') as pbar:
                for _ in pool.imap_unordered(self._dicom_to_jpeg, dicom_files):
                    pbar.update(1)

        self._write_corrupted_files_csv()

    def _get_dicom_files(self):
        dicom_files = []
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.dcm'):
                    dicom_files.append(os.path.join(root, file))
        return dicom_files

    def _create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _dicom_to_jpeg(self, file_path):
        try:
            dicom = pydicom.read_file(file_path)
            img = self._convert_to_grayscale(dicom.pixel_array)
            file_name = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
            out_path = os.path.join(self.output_dir, file_name)
            img = Image.fromarray(img, mode='L')
            img.save(out_path)
        except Exception as e:
            self._handle_error(file_path, e)

    def _convert_to_grayscale(self, img):
        img = img.astype(np.float32)
        img -= np.min(img)
        img /= np.max(img)
        img *= 255
        return img.astype(np.uint8)

    def _handle_error(self, file_path, error):
        self.num_corrupted_files += 1
        self.corrupted_files.append([file_path, str(error)])

    def _write_corrupted_files_csv(self):
        if self.num_corrupted_files > 0:
            with open('corrupted_files.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['File', 'Error'])
                writer.writerows(self.corrupted_files)

def run_conversion(input_dir, output_dir, num_processes=None):
    converter = DicomToJpegConverter(input_dir, output_dir, num_processes)
    converter.convert()
    if converter.num_corrupted_files > 0:
        print(f"Number of corrupted files: {converter.num_corrupted_files}")
        print("List of corrupted files:")
        for file, error in converter.corrupted_files:
            print(f"{file}: {error}")
    else:
        print("Conversion completed successfully.")

input_dir = '/system/user/publicdata/MIMIC_CXR/MIMIC_CXR'
output_dir = '/system/user/publicdata/MIMIC_CXR/hageneder/JPG'
num_processes = 24  # number of processes to use for multiprocessing

run_conversion(input_dir, output_dir,num_processes)