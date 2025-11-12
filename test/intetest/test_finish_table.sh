cd /Users/aatrox.wu/git/bbmail
source .venv/bin/activate

/usr/bin/time -l \
uv run python src/convert.py \
    --input_path [test/data/input.xlsx] \
    --output_path [test/result/output.xlsx]

# check result as expect
cmp -s test/data/ans.xlsx test/result/output.xlsx && \
    echo "Same, pass the test" || \
    echo "Different, fail the test" && \

# check created orig
if [ -f "test/result/output_orig.xlsx" ]; then
    echo "created orig"
else
    echo "orig not found"
fi

read -p "Press Enter to reset..."

# reset output orig
rm -f test/result/output.xlsx
mv test/result/output_orig.xlsx test/result/output.xlsx
