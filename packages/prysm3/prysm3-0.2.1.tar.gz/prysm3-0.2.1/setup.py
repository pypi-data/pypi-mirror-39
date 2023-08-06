from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prysm3',
    version='0.2.1',
    description="open-source tools for PRoxY System Modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='Sylvia Dee, Amir Allam, and Feng Zhu',
    url='https://github.com/fzhu2e/PRYSM',
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='prysm3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
