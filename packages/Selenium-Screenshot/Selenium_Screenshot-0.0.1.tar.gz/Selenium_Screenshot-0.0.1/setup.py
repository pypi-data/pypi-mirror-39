import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Selenium_Screenshot",
    version="0.0.1",
    author="Sayar Mendis",
    author_email="sayarmendis26@gmail.com",
    description="Selenium Screenshot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam4u3/Selenium_Screenshot.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)