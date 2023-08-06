import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdnagini",
    version="0.0.1",
    author="Ykäz Mihar",
    author_email="zaky@femaledaily.com",
    description="File Watcher",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': 'nagini=fdnagini.main:main'
    }
    # scripts=['bin/nagini']
)