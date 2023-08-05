import os
import sys

import setuptools  # Don't delete, hook for distutils

from distutils.core import setup

sys.path.insert(0, "src")

from qiq import qiq

setup(
	name="qiq",
	version=qiq.__version__,
	long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
	long_description_content_type="text/markdown",
	package_dir={"qiq": "src/qiq"},
	entry_points={
        "console_scripts": [
            "qiq = qiq.qiq:main",
        ],
    },
	packages=["qiq"],
    author="Alexander Ptakhin",
    author_email="me@aptakhin.name",
    description="qiq is the thin layer over pip with a few rules.",
    license="MIT",
    keywords="pip qiq",
    url="https://gitlab.com/aptakhin/qiq",
    project_urls={
        "Source Code": "https://gitlab.com/aptakhin/qiq",
    },
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: MacOS",
		"Operating System :: Microsoft",
		"Operating System :: POSIX",
		"Operating System :: Unix",
		"Programming Language :: Python",
		"Topic :: Software Development",
		"Topic :: Software Development :: Testing",
		"Topic :: Software Development :: Version Control",
		"Topic :: Utilities",
	],
)
