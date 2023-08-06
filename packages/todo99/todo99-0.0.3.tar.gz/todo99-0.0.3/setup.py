

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="todo99",
    version="0.0.3",
    author="plant99",
    author_email="shivashispadhi@gmail.com",
    description="Minimal todo app implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plant99/todo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points= {
        "console_scripts" : ['todo99=todo.__main__:maingl']
    }
)


