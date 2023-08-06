import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-distributed-users",
    version="0.0.1",
    author="Brendan Kamp",
    author_email="brendankamp757@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Spazzy757/django-distributed-users",
    packages=['distributed_user'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
