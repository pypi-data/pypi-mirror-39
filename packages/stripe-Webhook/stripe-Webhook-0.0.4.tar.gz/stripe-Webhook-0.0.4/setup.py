import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stripe-Webhook",
    version="0.0.4",
    author="maximeV",
    author_email="vermande.maxime@gmail.com",
    description="a package for stripe webhook",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://gitlab.com/maximeV/nowhatstripet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)