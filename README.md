1. install
win search: PowerShell, enter
```
cd  
mkdir git
cd git
git clone https://github.com/WuKobeWu/bb_costco_table.git
cd bb_costco_table
git checkout mvp
```

2. env
install python, uv
```
winget install Python.Python.3.12
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
use uv
```
uv venv
.\.venv\Scripts\Activate.ps1
```

3. use kit
download both: TW_OOS_ECOM_TMR.XLSX, F&S Daily OOS Recap_Taiwan .xlsx from email   
rename F&S Daily OOS Recap_Taiwan .xlsx as output.xlsx   
copy below to powershell but DONT PRESS ENTER
```
uv run python src/convert.py --input_path ${input_path} --output_path ${output_path} --result_path test/result/result_ashley_${date}.xlsx
```
right click TW_OOS_ECOM_TMR.XLSX, copy dir name -> ${ input_path}   
(same for ${ output_path})   
${date} = yyyymmdd ex: 20251130   
everything copied, press enter   

4. expect output
F&S Daily OOS Recap_Taiwan .xlsx        -> result, plz check if ok
F&S Daily OOS Recap_Taiwan _orig.xlsx   -> saved for safety, can del if above ok
plz write comment [here](https://docs.google.com/document/d/11MLShYlC4Ecna0u2Pyy2pFiZA3XZWi4XNtLadAvad2I/edit?usp=drive_link)





