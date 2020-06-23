#!/bin/bash

#
# Script to compile icons and search strings for linguistics in all project
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
    pyrcc5 ../icons/iconos.qrc -o ../app/iconos_rc.py
}

function build_UiFiles {
    cd ..
    for input_file in ui/*
    do
        output_file=${input_file/.ui/_Ui.py}
        echo -e "\t'$input_file' to '$output_file'..."
        pyuic5 -o app/$output_file $input_file
    done
}

# create project file
function build_project_file {
    echo " " > qtradingview.pro
    # python files
    find . -type f -name "*.py" | while read filename
    do
        echo "SOURCES += $filename" >> qtradingview.pro
    done
    # # ui files
    # find . -type f -name "*.ui" | while read filename
    # do
    #     echo "FORMS += $filename" >> qtradingview.pro
    # done
    # translations
    echo "TRANSLATIONS += app/i18n/en_EN.ts" >> qtradingview.pro
    echo "TRANSLATIONS += app/i18n/es_ES.ts" >> qtradingview.pro
    pylupdate5 -noobsolete qtradingview.pro
    lrelease qtradingview.pro
}


current_dir=$(pwd)
script_path=$(realpath $0)
script_dir=$(dirname $script_path)
cd $script_dir

# main

header

info "Icon Resources"
build_icons

echo -e "\n"

build_UiFiles

echo -e "\n"

info "Project File"
build_project_file

rm qtradingview.pro
echo -e "\n"