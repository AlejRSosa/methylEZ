from setuptools import setup, find_packages

setup(
    name="methylEZ",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "methylEZ = main:main",  # Ensure this points to main.py
        ],
    },
)
