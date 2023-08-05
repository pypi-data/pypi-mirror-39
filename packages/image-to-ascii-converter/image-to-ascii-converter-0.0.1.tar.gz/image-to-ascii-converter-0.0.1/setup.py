import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "sketchingdev", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about['__name__'],
    version=about['__version__'],
    description="Convert an image to ASCII",
    url="https://github.com/SketchingDev/image-to-ascii-converter",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Pillow>=5.0.0, <6.0.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.4"
    ],
    python_requires=">=3.4"
)
