import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="compbaseball",
    version="0.1.2",
    author="Hank Doupe",
    author_email="henrymdoupe@gmail.com",
    description="Documents COMP via baseball data examples.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdoupe/compbaseball",
    packages=setuptools.find_packages(),
    data_files=[("./", ["compbaseball/inputs.json"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
