import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="slime_mind",
    version="2.0.0",
    author="Alex Havermann, Ian Kottman",
    description="AI competition game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teofrastusb/SlimeMind",
    packages=setuptools.find_packages(),
    install_requires=['arcade'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)