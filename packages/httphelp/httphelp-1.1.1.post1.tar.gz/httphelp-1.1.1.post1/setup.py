try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    name="httphelp",
    description="Like man pages, but for HTTP status codes and headers (and more)",
    version="v1.1.1-post1",
    install_requires=["pyyaml", "urwid"],
    packages=["httphelp"],
    entry_points={"console_scripts": ["httphelp = httphelp.statcode:main"]},
    include_package_data=True,
    python_requires=">=3",
    url="https://github.com/Malex/statcode",
    author="Malex",
    author_email="malexprojects@gmail.com",
    license="MIT"
)
