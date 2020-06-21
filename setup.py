import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qtradingview",
    version="0.35.0",
    author='katmai',
    author_email='katmai.mobil@gmail.com',
    description='PyQt5 GUI for TradingView',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katmai1/qtradingview",
    packages=setuptools.find_packages(exclude=["*.egg-info", ]),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'qtradingview=qtradingview.__main__:main',
        ],
    },
    install_requires=[
        'docopt', 'peewee', 'PyQtWebEngine', 'toml', 'coloredlogs', 'ccxt',
    ],
)
