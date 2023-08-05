import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kml-sdk",
    version="0.0.4",
    author="zhusichuang",
    author_email="zhu_sichuang@163.com",
    description="KMl_SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'python-etcd>=0.4.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
)
