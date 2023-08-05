import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fbmmsg",
    version="0.0.3",
    author="Appvelox LLC",
    author_email="team@appvelox.ru",
    description="Simple but yet functional library for building Facebook Messenger bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AppVelox/fbmsg",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.6',
)
