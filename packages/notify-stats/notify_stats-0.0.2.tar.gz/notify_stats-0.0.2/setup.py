import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notify_stats",
    version="0.0.2",
    author="Ghayoor",
    author_email="",
    description="Send stats to email(s) in HTML format.",
    long_description="Send your scrapy stats to email(s)",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)