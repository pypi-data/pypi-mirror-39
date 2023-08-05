import setuptools  # Don't delete, hook for distutils

from distutils.core import setup

import src.qiq as qiq

setup(
	name="qiq",
	version=qiq.__version__,
	package_dir={"qiq": "src/qiq"},
	entry_points={
        "console_scripts": [
            "qiq = qiq.qiq:main",
        ],
    },
	packages=["qiq"],
	scripts=["src/qiq/qiq.py"],
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
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: Python Software Foundation License",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: POSIX",
		"Programming Language :: Python",
	],
)
