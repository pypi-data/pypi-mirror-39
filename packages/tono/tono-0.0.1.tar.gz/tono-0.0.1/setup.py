import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tono",
    version="0.0.1",
    author="Obie",
    author_email="obyaltha@example.com",
    description="A very simple script in web frameword for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Robialta/pybie",
    packages=setuptools.find_packages(),
    gui_scripts=['bin/pybie'],
    scripts=['bin/pybie.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


