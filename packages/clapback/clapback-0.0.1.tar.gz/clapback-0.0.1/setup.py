from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clapback",
    version="0.0.1",
    author="Alex Harston",
    author_email="alex@harston.io",
    description="A command-line tool to add clap emojis to your sentences.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexharston/clapback",
    license="MIT",
    python_requires='>=3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='clapback clap clapping emoji',
    packages=find_packages(),
    install_requires=['argparse',],
)