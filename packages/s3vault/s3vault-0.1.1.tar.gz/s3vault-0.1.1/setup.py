import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3vault",
    version="0.1.1",
    author="SchoolOrchestration",
    author_email="tech@appointmentguru.co",
    description="...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/.../...",
    packages=['s3vault'],
    install_requires=['requests', 'boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

