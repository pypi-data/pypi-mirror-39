import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymacroms",
    version="0.2.0",
    author="Kevin De Bruycker and Tim Krappitz",
    author_email="kevindebruycker@gmail.com",
    description="pyMacroMS - High performance quantification of complex high resolution polymer mass spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://macroarc.org/research/pymacroms.html",
    license="GNU GPLv3",
    packages=setuptools.find_packages(),
    install_requires=["IsoSpecPy>=1.9,<2", "matplotlib", "numpy", "pandas", "progressbar2", "reportlab", "sklearn", "svglib>=0.9.0b0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)