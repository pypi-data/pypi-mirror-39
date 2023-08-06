import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mona_client",
    version="0.0.8",
    author="MonaLabs",
    author_email="itai@monalabs.io",
    description="Client code for python Mona instrumentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/itai4/mona-python-client",
    download_url='http://pypi.python.org/pypi/mona-client/',
    packages=setuptools.find_packages(),
    install_requires=['mona-fluent-logger', 'watchdog'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={'mona_client': ['certs/fluentd.crt']})
