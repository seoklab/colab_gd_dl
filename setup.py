from setuptools import setup, find_namespace_packages

setup(
    name="galaxydock_dl",
    version="0.1.0",
    url="https://github.com/seoklab/galaxydock_dl",
    description="GalaxyDock-DL: Protein-Ligand Docking by Global Optimization and Neural Network Energy",
    author="Changsoo Lee",
    author_email="ccaa2013@snu.ac.kr",
    python_requires=">=3.7",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    package_data={
        "gd_dl.bin": ["*"],
        "gd_dl.data": ["*"],
    },
    install_requires=[
    ],
)
