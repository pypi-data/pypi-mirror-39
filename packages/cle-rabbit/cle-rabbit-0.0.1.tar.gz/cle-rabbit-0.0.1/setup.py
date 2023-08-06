import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cle-rabbit",
    version="0.0.1",
    author="Mikhail Kedrovskiy",
    author_email="author@example.com",
    description="Connect with RabbitMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        "pika",
    ],
)