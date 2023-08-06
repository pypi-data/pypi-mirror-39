from setuptools import setup

__project__ = "camera"
__version__ = "1.3.0"
__description__ = "A Python module to use a PiCamera easily"
__packages__ = ["camera"]
__author__ = "Arca Ege Cengiz"
__author_email__ = "arcaegecengiz@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["camera","raspberry pi", "PiCamera", "learning"]
__requires__ = ["time","picamera"]


setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    requires = __requires__,
)
