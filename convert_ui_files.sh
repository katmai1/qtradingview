echo -e "\n"
pyrcc5 ico/iconos.qrc -o iconos_rc.py
for input_file in ui/*
do
    echo " Conviertiendo fichero '$input_file'..."
    output_file=${input_file/.ui/.py}
    pyuic5 -o src/$output_file $input_file
done

