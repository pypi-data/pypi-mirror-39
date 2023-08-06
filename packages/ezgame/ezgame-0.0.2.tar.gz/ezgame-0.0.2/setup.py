import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezgame",
    version="0.0.2",
    author="Fabricio J.C. Montenegro",
    author_email="fabriciojcmontenegro@gmail.com",
    description="Small layer over pygame to make its usage more transparent.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SplinterDev/ezgame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Multimedia :: Graphics :: Viewers",
    ],
    install_requires=["pygame", "point2d"]
)