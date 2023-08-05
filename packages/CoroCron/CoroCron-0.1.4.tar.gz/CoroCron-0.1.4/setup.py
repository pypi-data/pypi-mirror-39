import io
import CoroCron
from setuptools import setup, find_packages

try:
    with io.open('readme.md') as reader:
        readme = reader.read()
except:
    readme = ""

setup(
    name = "CoroCron",
    version = CoroCron.__version__,
    author = "Flying Kiwi",
    author_email = "github@flyingkiwibird.com",
    description = ("A pythonic cron using asyncio"),
    license = "MIT",
    keywords = "Cron asyncio schedule",
    url = "https://github.com/FlyingKiwiBird/EsiPysi",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "examples", "examples.*"]),
    install_requires=[],
    long_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
