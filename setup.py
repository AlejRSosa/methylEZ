from setuptools import setup, find_packages

setup(
    name="methylEZ",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyperclip",
        "ttkthemes",
        "biopython",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "methylEZ = methylEZ.main:main",  # Ensure this points to main.py
        ],
    },
)
