from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fc-config",
    version='0.1.5',
    packages=find_packages(exclude=["test"]),
    url="http://git.fairsense.cn",
    license="Fairsense License 1.0",
    author="wengyingjie",
    author_email="yingjie.weng@fairsense.cn",
    description="fairsense config center sdk",
    install_requires=[],

)
