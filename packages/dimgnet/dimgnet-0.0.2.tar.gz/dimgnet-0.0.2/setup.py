import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dimgnet",
    version="0.0.2",
    author="Mai Tu Duy",
    author_email="maituduy1998@gmail.com",
    description="download imagenet package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['dimgnet=dimgnet.download_img:main'],
    },
)
