from setuptools import setup, find_packages

setup(
    name="boltscraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    python_requires=">=3.8",
)
