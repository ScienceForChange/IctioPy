import pathlib
from setuptools import setup
WD = pathlib.Path(__file__).parent
README = (WD / "README.md").read_text()
setup(
    name="ictiopy",
    version="1.0.0",
    description="Parse observations from ictio.org's Citizen Observatory",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ScienceForChange/IctioPy",
    author="Alex Amo (Science for Change) and Ana Álvarez (ICM-CSIC)",
    author_email="alex.amo@scienceforchange.eu",
    license="EUPL1.2",
    classifiers=[
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta"
    ],
    packages=["ictiopy"],
    package_dir={'ictiopy': '.'},
    include_package_data=True,
    install_requires=["pandas", "numpy", "excel_fast_load"],
)
