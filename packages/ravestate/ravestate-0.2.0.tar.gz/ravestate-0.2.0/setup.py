import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_uris = []
required = []
with open("requirements.txt", "r") as freq:
    for line in freq.read().split():
        if "://" in line:
            required_uris.append(line)
        else:
            required.append(line)


setuptools.setup(
    name="ravestate",
    version="0.2.0",
    url="https://github.com/roboy/ravestate",
    author="Roboy",
    author_email="info@roboy.org",

    description="Ravestate is a reactive library for real-time natural language dialog systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    package_dir={'': 'modules'},
    packages=setuptools.find_packages("modules"),
    include_package_data=True,
    scripts=["rasta"],

    install_requires=required,
    dependency_links=required_uris,
    python_requires='>=3.6',

    # TODO: Add classifiers
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
)
