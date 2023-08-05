import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vampireanalysis",
    version="3.0.9",
    author="Kyu Sang Han",
    author_email="khan21@jhu.edu",
    description="Vampire Image Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wirtzlab.johnshopkins.edu",
    packages=setuptools.find_packages(),
    install_requires=[
        'scipy==1.1.0',
        'pandas==0.23.4',
        'numpy==1.15.4',
        'pillow==5.3.0',
        'matplotlib==2.2.3',
        'scikit-learn==0.20.0',
        'opencv-python==3.4.3.18',
    ],
    scripts=['bin/vampire.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ),
)