values=(73 75 33 92 445 99 77 26 67 34)

pip install numpy > /dev/null
pip install scikit-learn > /dev/null
pip install pandas > /dev/null


# Loop over the array of values and run the Python program with each value
for value in "${values[@]}"
do
     python3 ./main.py "$value"
done

