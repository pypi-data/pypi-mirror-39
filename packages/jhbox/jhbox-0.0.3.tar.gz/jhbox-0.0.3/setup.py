import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jhbox",
    version="0.0.3",
    author="Chen Jinhao",
    author_email="jin_hao_chen@163.com",
    description="A Python Tool Box",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jin-hao-chen/jhbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

