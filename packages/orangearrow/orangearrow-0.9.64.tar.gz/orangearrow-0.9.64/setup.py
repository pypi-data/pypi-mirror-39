from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="orangearrow",
    description="A Python Library for interacting with the Amazon Product Advertising API.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="v0.9.64",
    author='Joe Wilson',
    license='Apache2',
    url="https://github.com/wreddily/orangearrow",
    packages=['orangearrow'],
    python_requires='>=3.4',
    install_requires=[
        "requests>=2.20.0",
        "xmltodict>=0.10.2",
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
