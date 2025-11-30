import argparse
from datetime import timedelta
import pandas as pd
import shutil
import openpyxl

##### configs #####
global SHEET_NAME
SHEET_NAME = "D13"
ROW_NAME = "Out Of Stock By Warehouse_Ecomm"
INPUT_COL_LIST = ["Dept", "Item", "English Description", "Item Status", "OH", "OO"]
OUTPUT_COL_LIST = ["Dept", "Item", "English Description", "Item Status", "OH", "OO", "Arrival Date", "Comment", "Local item", "ICS"]
##### configs #####

class Convert:
    def __init__(self, args):
        self.args = args
        self.input_path = args.input_path
        self.output_path = args.output_path
        self.result_path = args.result_path


    def convert(self):
        input = self._read_input()
        output, startrow = self._read_output(SHEET_NAME)
        output = self._keep_same_row(input, output)
        output = self._add_new_row(input, output)
        output = self._add_date(output)
        output = self._sort(output, self.args)

        self._make_copy(self.args)
        # FIXME: refactor: make output & output indep, no call output reference both
        self._clear_old_row(SHEET_NAME, startrow)
        self._put_2_fs(output, self.args, SHEET_NAME, startrow)
        self._save(output)
        
        return output
    
    def _read_input(self):
        input = pd.read_excel(self.input_path, usecols=INPUT_COL_LIST)
        input = input[input["Dept"] == 13]
        input.reset_index(drop=True, inplace=True)
        return input
    
    def _read_output(self, sheet_name):
        output_all = pd.read_excel(self.output_path, header=None, sheet_name=sheet_name)

        idx = output_all[output_all.iloc[:, 0] == ROW_NAME].index[0]
        output = pd.read_excel(self.output_path, skiprows=idx+1, sheet_name=sheet_name, usecols=OUTPUT_COL_LIST)
        return output, idx+1
    
    def _keep_same_row(self, input, output):
        input_same_row = input[input["Item"].isin(output["Item"])]
        output_same_row = output[output["Item"].isin(input["Item"])]
        output_col = [c for c in output.columns if c not in input.columns]
        output = pd.merge(input, output, on="Item", how="left")

        return output
    
    def _add_new_row(self, input, output):
        new_rows = input[~input["Item"].isin(output["Item"])]
        if new_rows.empty:
            return output
        output = pd.concat([output, new_rows])
        return output
    
    def _add_date(self, output):
        today = pd.Timestamp.now().normalize()
        yesterday = today - timedelta(days=1)
        output["Arrival Date"] = output["Arrival Date"].apply(self.date_clean_convert, yesterday=yesterday)
        return output
    
    def _sort(self, output, args):
        if not hasattr(args, "sort_by") or args.sort_by is None:
            args.sort_by = "Arrival Date"
        if not hasattr(args, "ascending") or args.ascending is None:
            args.ascending = False
        
        output = output.sort_values(by=args.sort_by, ascending=args.ascending)
        return output

    def _make_copy(self, args):
        shutil.copy(self.output_path, self.output_path.replace(".xlsx", "_orig.xlsx"))
        return None

    def date_clean_convert(self, val, yesterday):
        if pd.isna(val):
            return "today"
        if str(val).strip().lower() == "today":
            return yesterday.strftime('%Y/%m/%d')
        if isinstance(val, (int, float)):
            time_val = pd.Timestamp("1899-12-30") + pd.Timedelta(days=val)
            return time_val.strftime('%Y/%m/%d')
        return val.strftime('%Y/%m/%d')
    
    def _clear_old_row(self, sheet_name, startrow):
        wb = openpyxl.load_workbook(self.output_path)
        ws = wb[sheet_name]
        startrow += 1
        endrow = startrow + 100 + 1
        endcol = 100
        for row in range(startrow, endrow):
            for col in range(1, endcol):
                ws.cell(row=row, column=col).value = None

        wb.save(self.output_path)
        return None
    
    def _put_2_fs(self, output, args, sheet_name, startrow):
        with pd.ExcelWriter(
            self.output_path,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="overlay",
        ) as writer:
            output.to_excel(
                writer,
                sheet_name=SHEET_NAME, 
                startrow=startrow,
                startcol=0,
                header=True,
                index=False
                )
        return None

    def _save(self, output):
        output.to_excel(self.result_path, index=False)

        print(f"convert finished! luv u py <3 <3 <3")
        print(f"output saved to {self.result_path}")
        return output

    def _put_orig_back(self, args):
        if not hasattr(args, "test") or args.test is None or not args.test:
            return None
        os.remove(self.output_path)
        os.rename(self.output_path.replace(".xlsx", "_orig.xlsx"), self.output_path)
        return None

def parse_args():
    # FIXME: make arg take any vale
    parser = argparse.ArgumentParser(description='Convert Excel file')
    parser.add_argument('--input_path', type=str, required=True, help='Input Excel file')
    # FIXME: this is not output, it is output format, refactor
    parser.add_argument('--output_path', type=str, required=True, help='Output Excel file')
    parser.add_argument('--result_path', type=str, required=True, help='Result Excel file')
    parser.add_argument('--sort_by', type=str, required=False, help='Sort by column')
    parser.add_argument('--ascending', type=bool, required=False, help='Sort ascending')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    convert_instance = Convert(args)
    convert_instance.convert()