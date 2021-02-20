import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcframework",  # Replace with your own username
    version="1.4.1",
    author="Rayyan Cyclegar",
    author_email="aboominister@gmail.com",
    description="A Python micro web framework for creating dynamic websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbooMinister25/arc",
    packages=["arc", ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'webob', "cherrypy", "whitenoise", "parse", "jinja2"
    ],
    include_package_data=True,
    package_data={
        "arc": ["selfpages/*.html", "static/*.css"],
    }
)

