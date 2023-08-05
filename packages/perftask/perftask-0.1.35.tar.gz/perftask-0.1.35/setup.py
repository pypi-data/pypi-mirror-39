import setuptools
import os
import sys

here = os.path.dirname(__file__)
if sys.version_info >= (3, 0):
    from importlib import __import__ as perftask_import
else:
    perftask_import = __import__

sys.path.insert(0, os.path.join(here, "perftask"))
help_mod = perftask_import("help")
sys.path.pop(0)

name = "perftask"
version = help_mod.__version__
author = "Youngsung Kim"
author_email = "grnydawn@gmail.com"
desc = "The Tasking Platform"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=desc,
    packages=[
        "perftask",
        "perftask.platform",
        "perftask.flowctrtask",
        "perftask.stdtask",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ],
    install_requires=["toml", "virtualenv", "pipenv"],
    entry_points={
        "console_scripts": [
            "perform=perftask.entry:main",
        ],
    },
)
        #"License :: OSI Approved :: GNU GPLv3",
