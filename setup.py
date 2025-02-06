from setuptools import setup, find_packages

setup(
    name="methylEZ",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "pandas",
        "pyperclip",
    ],
    entry_points={
        "gui_scripts": [
            "methylEZ = main:main",  # run 'methylEZ' via command line
        ],
    },
)
