import os
from setuptools import setup


def read(*pathnames):
    return (
        open(os.path.join(os.path.dirname(__file__), *pathnames), "rb")
        .read()
        .decode("utf-8")
    )


version = "2.0.0.dev0"

setup(
    name="collective.complexrecordsproxy",
    version=version,
    description="Providing a proxy class for plone.registry allowing IObject fields to be stored as separate records using the plone.registry collection support.",
    long_description="\n".join(
        [
            read("README.md"),
            read("CONTRIBUTORS.md"),
            read("CHANGES.md"),
        ]
    ),
    long_description_content_type="text/markdown",
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="configuration registry",
    author="Sune Broendum Woeller",
    author_email="sune@woeller.dk",
    url="http://pypi.python.org/pypi/collective.complexrecordsproxy",
    license="GPLv2+",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=["plone.registry>=1.0"],
    entry_points="""
      """,
)
