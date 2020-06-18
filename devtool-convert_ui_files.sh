#
# Script to convert qt ui files and resources to python files
#

function header {
    echo -e "\n#"
    echo "# QTradingView - devtool"
    echo -e "#\n"
}

function info {
    echo -e " [i] $1"
}

#

function build_icons {
    echo -e "\tFile: 'icons/iconos.qrc'"
    pyrcc5 icons/iconos.qrc -o app/iconos_rc.py
}

#

function build_UiFiles {
    for input_file in ui/*
    do
        output_file=${input_file/.ui/_Ui.py}
        echo -e "\t'$input_file' to '$output_file'..."
        pyuic5 -o app/$output_file $input_file
    done
}

#

function build_project_file {
    cd app
    echo " " > qtradingview.pro
    find . -type f -name "*.py" | while read filename
    do
        echo "SOURCES += $filename" >> qtradingview.pro
    done
    echo "TRANSLATIONS += i18n/en_EN.ts" >> qtradingview.pro
    echo "TRANSLATIONS += i18n/es_ES.ts" >> qtradingview.pro
    pylupdate5 -noobsolete qtradingview.pro
    # pylupdate5 qtradingview.pro
    lrelease qtradingview.pro
}

# inicio

header

info "Icon Resources"
build_icons

info "Ui Files"
build_UiFiles

build_project_file
