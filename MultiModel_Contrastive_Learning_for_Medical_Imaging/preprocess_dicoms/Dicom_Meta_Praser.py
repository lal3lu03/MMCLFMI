import pydicom
import pandas as pd
import os
from pathlib import Path
from tqdm.notebook import tqdm
import json
import sys
from multiprocessing import Pool


class DicomParser:
    def __init__(self, data_path, out_path, json_path=None, number=None):
        self.data_path = data_path
        self.out_path = out_path
        self.json_path = json_path
        self.number = number

    def get_infos_meta(self, ds):
        """
        get all metadata from a dcm file without the image data
        """

        tmp_dict = {}
        for elem in ds:
            if elem.VR == 'SQ':
                # Exclude LUTs because they're huge and not human readable
                if 'LUT' not in elem.name:
                    [self.get_infos_meta(item) for item in elem]
            else:
                e = elem.tag.group << 16 | elem.tag.element
                # save the values in a dictionary without the image array
                if hasattr(elem.value, '__len__'):
                    if len(elem.value) > 100:
                        tmp_dict[e] = None
                    else:
                        if isinstance(elem.value, pydicom.multival.MultiValue):
                            tmp_dict[e] = list(elem.value)
                        else:
                            tmp_dict[e] = elem.value
                else:
                    if isinstance(elem.value, pydicom.multival.MultiValue):
                        tmp_dict[e] = list(elem.value)
                    else:
                        tmp_dict[e] = elem.value
        return tmp_dict

    def parse(self):
        """
        Parses the dicom files and saves them as a csv and json file.
        """

        base_path = Path(self.data_path)
        out_filename = self.out_path
        if self.json_path is not None:
            json_filename = self.json_path
        else:
            json_filename = out_filename
            if json_filename.endswith('.gz'):
                json_filename = json_filename[:-3]
            if json_filename.endswith('.csv'):
                json_filename = json_filename[:-4]
            json_filename += '.json'

        # get list of all dicoms under the given path
        files = [str(path) for path in base_path.rglob('*.dcm')]

        N = len(files)
        print(f'Found {N} files.')
        if self.number is not None:
            if self.number < N:
                # limit the number of dicoms
                print(f'Limiting parsing to {self.number} of {N} DICOMs.')
                N = self.number

        if N == 0:
            print('No files to process. Exiting.')
            sys.exit()

        dicom_tabular_data = []
        with open(json_filename, 'w') as fp:
            # initialize the array in the json file
            fp.write('[\n')

            for i in tqdm(range(N)):
                if i > 0:
                    fp.write(',\n')
                dicom_full_path = files[i]

                # dicom filename is the last name in the file path
                fn = os.path.basename(dicom_full_path).split('.')[0]

                # prepare the json output as a dictionary with this dicom filename as key
                fp.write('{')
                fp.write(f'"{fn}": ')

                # load info from dicom
                plan = pydicom.filereader.dcmread(dicom_full_path, stop_before_pixels=True, force=True)

                field_dict = {}
                dicom_json = {}

                # go through each element in the dicom
                for elem in plan:
                    e = (elem.tag.group << 16) | elem.tag.element

                    # sequence data -> JSON
                    if elem.VR == 'SQ':
                        field_dict[e] = len(elem.value)
                        if 'LUT' not in elem.name:
                            dicom_json[e] = [self.get_infos_meta(item) for item in elem]
                    else:
                        # three "real" data-types: number, string, or list of things
                        field_dict[e] = elem.value

                # add the dicom filename to the dictionary
                field_dict['dicom'] = fn
                dicom_tabular_data.append(field_dict)

                # convert the dictionary to json
                js = json.dumps(dicom_json)

                # write the json to the file
                fp.write(js)
                # finish the json entry
                fp.write('}')

            # finish the json file
            fp.write('\n]')
            fp.close()

        # convert the list of dictionaries to a pandas dataframe
        df = pd.DataFrame(dicom_tabular_data)
        # set the dicom filename as the index
        df.set_index('dicom', inplace=True)

        # save the dataframe as a csv
        if out_filename.endswith('.gz'):
            df.to_csv(out_filename, compression='gzip')
        else:
            df.to_csv(out_filename)
