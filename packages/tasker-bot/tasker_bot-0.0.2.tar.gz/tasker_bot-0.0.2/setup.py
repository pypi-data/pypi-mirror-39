import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tasker_bot",
    version="0.0.2",
    author="Edwin Ariza",
    author_email="me@edwinariza.com",
    description="Bot para gestionar y automatizar la gestión de tareas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['tasker'],
    url="https://bitbucket.org/edwinariza/tasker_bot/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)