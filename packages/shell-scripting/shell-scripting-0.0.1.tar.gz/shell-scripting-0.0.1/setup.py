import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shell-scripting",
    version="0.0.1",
    author="whoami",
    author_email="whoami@systemli.org",
    description="Shortcut functions for shell scripting on Python 3.7+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/whoizit/shell-scripting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    license='UNLICENSE'
)
