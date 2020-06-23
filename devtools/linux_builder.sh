#!/bin/bash

#
# ─── CONSTANTES ─────────────────────────────────────────────────────────────────
#

VERSION=$(cat .VERSION)
DIST_PATH="devtools/dist"
WORK_PATH="devtools/build"

#
# ─── FUNCIONES ──────────────────────────────────────────────────────────────────
#

function clean_devtools_folder {
    rm -rf $WORK_PATH
    rm -rf $DIST_PATH
}


function clean_pycache {
    find . -name '*.pyc' -type f -delete
    find . -name '__pycache__' -type d -delete
    rm qtradingview.spec
}

# ejecuta pyinstaller
function pyinstaller_run {
    pyinstaller -y --clean --onefile --name qtradingview \
        --distpath $DIST_PATH \
        --workpath $WORK_PATH \
        --add-data "app/i18n:app/i18n" \
        --add-data "ui:ui" \
        apprun.py
}

# se asegura de ejecutarlo desde la carpeta correcta
function check_running_path {
    current_dir=$(pwd)
    script_path=$(realpath $0)  # busca la carpeta de este script
    script_dir=$(dirname $script_path)
    cd $script_dir  # accedemos a ella y bajamos un nivel
    cd ..
}

function freeze_run {
    clean_devtools_folder   # limpia carpetas
    pyinstaller_run         # genera el binario
    clean_pycache           # limpia pycache
}

function debian_run {
    chmod 0755 $DIST_PATH'/qtradingview'
    size_bin=$(du -k $DIST_PATH'/qtradingview' | cut -f1)
    mkdir devtools/dist/qtradingview-$VERSION
    tar xvzf devtools/template_debian.tar.gz -C devtools/dist/qtradingview-$VERSION
    cp $DIST_PATH'/qtradingview' "devtools/dist/qtradingview-$VERSION/usr/bin/"
    cd devtools/dist/qtradingview-$VERSION
    echo "Installed-Size: $size_bin" >> DEBIAN/control
    echo "Version: $VERSION" >> DEBIAN/control
    cd ..
    dpkg-deb --build qtradingview-$VERSION
    # rm -rf qtradingview-$VERSION

}

function help_run {
    echo -e "\n  Usage:"
    echo -e "\t $0 freeze \t\t\t Build an executable file"
    echo -e "\t $0 debian \t\t\t Build a debian package"
    echo ""
}

#
# ─── MAIN ───────────────────────────────────────────────────────────────────────
#

# comprueba si estamos en la carpeta que toca
check_running_path

case $1 in
    freeze)
        echo -e "\n [i] Building executable...\n"
        freeze_run
        # renombra el fichero con la version
        mv "$DIST_PATH/qtradingview" "devtools/dist/qtradingview-$VERSION"
        echo -e "\n [i] File generated in '$(realpath devtools/dist)'\n"
    ;;
    debian)
        echo -e "\n [i] Building executable...\n"
        freeze_run
        debian_run
    ;;
    *)
        echo -e "\n[!] Option incorrect"
        help_run
    ;;
esac

