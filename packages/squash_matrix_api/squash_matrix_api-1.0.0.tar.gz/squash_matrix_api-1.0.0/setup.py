# coding: utf-8

"""
    Squash Matrix API

    # Endeavor The squash matrix API enables clubs, players, and regions to own their information, with results being updated weekly. The API information sits ontop of squash matrix australia website [https://squashmatrix.com](https://squashmatrix.com) # API Aside from the documentation provided below, there is also a `{json:api}` available and can be accessed in the same manner, with the addition of the accept header `{accept: application/vnd.api+json}`. More information about json api can be viewed on their website at [http://jsonapi.org/](http://jsonapi.org/) # Squash Matrix Scrapper There is a ruby SDK for retrieving information from [https://squashmatrix.com](https://squashmatrix.com) which can be found at https://rubygems.org/gems/squash_matrix # SDK's Please stay posted! Client sdk's for the following will be provided shortly:    - Javascript   - Java   - Ruby  # Blog Find relevent and interesting media on [wilkosz.com.au](http://wilkosz.com.au) # Contact Join this endeavor and be appart of the community [https://www.facebook.com/squashmatrixapi](https://www.facebook.com/squashmatrixapi) <hr />  # noqa: E501

    OpenAPI spec version: 1.0.0

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "squash_matrix_api"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Squash Matrix API",
    author="joshuawilkosz",
    author_email="joshuawilkosz@squashmatrix.io",
    url="https://github.com/wilkosz/squash_matrix_io_sdks/tree/master/python",
    keywords=["Swagger", "Squash Matrix API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    # Endeavor The squash matrix API enables clubs, players, and regions to own their information, with results being updated weekly. The API information sits ontop of squash matrix australia website [https://squashmatrix.com](https://squashmatrix.com) # API Aside from the documentation provided below, there is also a &#x60;{json:api}&#x60; available and can be accessed in the same manner, with the addition of the accept header &#x60;{accept: application/vnd.api+json}&#x60;. More information about json api can be viewed on their website at [http://jsonapi.org/](http://jsonapi.org/) # Squash Matrix Scrapper There is a ruby SDK for retrieving information from [https://squashmatrix.com](https://squashmatrix.com) which can be found at https://rubygems.org/gems/squash_matrix # SDK&#39;s Please stay posted! Client sdk&#39;s for the following will be provided shortly:    - Javascript   - Java   - Ruby  # Blog Find relevent and interesting media on [wilkosz.com.au](http://wilkosz.com.au) # Contact Join this endeavor and be appart of the community [https://www.facebook.com/squashmatrixapi](https://www.facebook.com/squashmatrixapi) &lt;hr /&gt;  # noqa: E501
    """
)
