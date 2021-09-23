from setuptools import setup, find_packages

setup(
    name="json2tree",
    version="0.1.0",
    description="Python package to create html tree view for json files.",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="https://github.com/abhaykatheria/json2tree",
    author="Abhay Katheria and Mithilesh Tiwari",
    author_email="abhay.katheria1998@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"console_scripts": ["json2tree=json2tree.__main__:main"]},
)
