import argparse

import pandas as pd

##### configs #####
global SHEET_NAME
SHEET_NAME = "D13"
##### configs #####

class Convert:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def convert(self):
        input, output = self._read(SHEET_NAME)
        self._copy_output(output)
        input, output = self._in2out(input, output)
        output = self._copy_col(output)
        output = self._del_table(output)
        self._save(output)
        print(f"convert finished! luv u py <3 <3 <3")
        print(f"output saved to {self.output_path}")
        return output
    
    def _read(self, sheet_name):
        input = pd.read_excel(self.input_path)
        input = input.iloc[:, 1:]
        input = input[input["Dept"] == 13]
        output_all = pd.read_excel(self.output_path, header=None, sheet_name=sheet_name)

        idx = output_all[output_all.iloc[:, 0] == "Out Of Stock By Warehouse_Ecomm"].index[0]
        output = pd.read_excel(self.output_path, skiprows=idx+1, sheet_name=sheet_name)
        return input, output

def parse_args():
    parser = argparse.ArgumentParser(description='Convert Excel file')
    parser.add_argument('--input_path', type=str, required=True, help='Input Excel file')
    parser.add_argument('--output_path', type=str, required=True, help='Output Excel file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    convert_instance = Convert(args.input_path, args.output_path)
    convert_instance.convert()