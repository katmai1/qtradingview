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
    pyrcc5 icons/iconos.qrc -o iconos_rc.py
}

# create project file
function build_project_file {
    echo " " > qtradingview.pro
    # python files
    find . -type f -name "*.py" | while read filename
    do
        echo "SOURCES += $filename" >> qtradingview.pro
    done
    # ui files
    find . -type f -name "*.ui" | while read filename
    do
        echo "FORMS += $filename" >> qtradingview.pro
    done
    # translations
    echo "TRANSLATIONS += i18n/en_EN.ts" >> qtradingview.pro
    echo "TRANSLATIONS += i18n/es_ES.ts" >> qtradingview.pro
    pylupdate5 -noobsolete qtradingview.pro
    lrelease qtradingview.pro
}


# main

header

info "Icon Resources"
build_icons

info "Project File"
build_project_file
