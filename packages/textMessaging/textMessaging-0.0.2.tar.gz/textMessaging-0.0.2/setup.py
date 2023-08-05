import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textMessaging",
    version="0.0.2",
    author="Will Roberts",
    author_email="willeroberts3@gmail.com",
    description="Python package to send text messages via smtp.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weroberts/py-text-messaging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
