"""Install arXiv auth package."""

from setuptools import setup, find_packages

setup(
    name='arxiv-auth',
    version='0.2.3',
    packages=[f'arxiv.{package}' for package
              in find_packages('./arxiv', exclude=['*test*'])],
    install_requires=[
        "pycountry",
        "sqlalchemy",
        "mysqlclient",
        "python-dateutil",
        "arxiv-base",
        "pyjwt",
        "redis",
        "redis-py-cluster"
    ],
    zip_safe=False
)
