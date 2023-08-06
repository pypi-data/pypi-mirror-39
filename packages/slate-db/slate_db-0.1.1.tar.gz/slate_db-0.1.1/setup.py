from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="slate_db",
    version="0.1.1",
    description="Wrapper for working with Slate databases.",
    long_description=readme(),
    url="https://github.com/jamie-r-davis/slate_db",
    author="Jamie Davis",
    author_email="jamjam@umich.edu",
    license="MIT",
    packages=["slate_db"],
    install_requires=['attrdict', 'pyodbc'],
    include_package_date=True,
    zip_safe=False)
