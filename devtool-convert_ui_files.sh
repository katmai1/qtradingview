#
# Script to convert qt ui files and resources to python files
#

echo -e "\n"
echo -e " [i] File 'icons/iconos.qrc' | Converting icons resource...\n"
pyrcc5 icons/iconos.qrc -o src/main/python/iconos_rc.py

# Conviertiendo UI files...
for input_file in ui/*
do
    output_file=${input_file/.ui/_Ui.py}
    echo -e " [i] Converting '$input_file' to '$output_file'..."
    pyuic5 -o src/main/python/$output_file $input_file
done

