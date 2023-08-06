import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msudft",
    version="0.0.1",
    author="Seong-Gon Kim",
    author_email="sk162@msstate.edu",
    description="Python tools for physics simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/msudft",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
