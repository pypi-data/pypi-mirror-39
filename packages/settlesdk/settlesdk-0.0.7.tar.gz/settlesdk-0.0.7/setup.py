import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="settlesdk",
    version="0.0.7",
    author="Adam Peretti",
    author_email="adam.peretti@gmail.com",
    description="The Settle SDK abstracts using the price feed and settle API by wrapping authentication in a function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SettleFinance/Settle-SDK-Python",
    packages=setuptools.find_packages(),
    install_requires=['PyJWT', 'python-dotenv', 'requests', 'cryptography'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)