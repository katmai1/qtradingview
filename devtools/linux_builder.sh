version=$(cat .VERSION)
version_folder="devtools/qtradingview-"$version

rm -rf devtools/build
rm -rf devtools/dist

pyinstaller -y --clean --onefile --name qtradingview \
    --distpath devtools/dist \
    --workpath devtools/build \
    --add-data "icons/logo.png:." \
    --add-data "ui:ui" \
    --upx-dir=/opt/upx/ \
    apprun.py

# mkdir -p $version_folder"/ui"
# mv devtools/dist/* $version_folder
# cp ui/* $version_folder"/ui/"
# cp icons/logo.png $version_folder

# elimina pycache
find . -name '*.pyc' -type f -delete
find . -name '__pycache__' -type d -delete