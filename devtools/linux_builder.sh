version=$(cat .VERSION)
version_folder="devtools/qtradingview-"$version

pyinstaller -y --clean --onefile --name qtradingview \
    --distpath devtools/dist \
    --workpath devtools/build \
    apprun.py

mkdir -p $version_folder"/ui"
mv devtools/dist/* $version_folder
cp ui/* $version_folder"/ui/"

find . -name '__pycache__' -type d -exec rmdir {}