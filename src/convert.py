import argparse

import pandas as pd


class Convert:
    input_path: str
    output_path: str

    def convert(self):
        input, output = self._read()
        self._copy_output(output)
        input, output = self._in2out(input, output)
        output = self._copy_col(output)
        output = self._del_table(output)
        self._save(output)
        print(f"convert finished! luv u py <3 <3 <3")
        print(f"output saved to {self.output_path}")
        return output
    
    def _read(self):
        input = pd.read_excel(self.input_path)
        output = pd.read_excel(self.output_path)
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