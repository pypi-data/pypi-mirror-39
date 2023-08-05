from setuptools import setup, find_packages

def readme() -> str:
    with open('./README.md') as f:
        return f.read()


setup(
    name="fluentd-log-handler",
    version='0.0.2',
    author="Hyun-Tae Hwang",
    author_email="hwanght1@gmail.com",
    description="Python logging handler for Fluentd",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license='GPL',
    url="https://github.com/neillab/fluentdloghandler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
    ],
)
