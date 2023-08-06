import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="side-kick",
    version="0.0.3",
    author="Ben Currie",
    author_email="benjamin.w.currie@gmail.com",
    description="A lightweight task runner",
    long_description=long_description,
    url="https://github.com/CurrieBen/sidekick",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
