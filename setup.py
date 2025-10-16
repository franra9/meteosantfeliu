from setuptools import setup, find_packages

setup(
    name="meteosantfeliu",
    version="0.0.1",
    author="Francesc Roura Adserias",
    author_email="francescrouradserias@gmail.com",
    description="Package to get climate reports from stations that report to xxxx",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    python_requires=">=3.7",
)
