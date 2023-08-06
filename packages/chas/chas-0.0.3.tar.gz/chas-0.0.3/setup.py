import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chas",
    version="0.0.3",
    author="Lukas Cerny",
    author_email="lukas.cerny@exponea.com",
    scripts=["script.py"],
    description="Framework for creating and running cron jobs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukasotocerny/chas",
    package_dir = {"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)