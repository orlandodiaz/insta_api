import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="insta_api",
    version="0.1.8",
    author="Orlando Diaz",
    author_email="orlandodiaz.dev@gmail.com",
    description="Unofficial instagram API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orlandodiaz/insta_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ['requests>=2.19.1', 'requests-toolbelt>=0.8.0', 'log3>=0.1.6']

)