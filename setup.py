from setuptools import setup, find_packages

setup(
    name="methylEZ",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # Ensure all files are included
    install_requires=[
        "pandas",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "methylEZ = methylEZ.main:main",  # Ensure correct package structure
        ],
    },
)
