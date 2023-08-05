import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

#packaging
setuptools.setup(
    name="prsync",
    version="0.0.11",
    author="Itay Bardugo",
    author_email="itaybardugo91@gmail.com",
    description="a GUI for rsync (linux servers)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['paramiko'],
    url="https://github.com/itay-bardugo/prsync/",
    dependency_links=["https://github.com/paramiko/paramiko/"],
    entry_points={
        "gui_scripts": [
            "prsync = prsync.main:main"
        ],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
