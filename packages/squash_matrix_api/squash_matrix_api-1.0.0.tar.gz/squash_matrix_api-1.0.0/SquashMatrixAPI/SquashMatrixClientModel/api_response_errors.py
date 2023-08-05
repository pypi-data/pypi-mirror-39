# coding: utf-8

"""
    Squash Matrix API

    # Endeavor The squash matrix API enables clubs, players, and regions to own their information, with results being updated weekly. The API information sits ontop of squash matrix australia website [https://squashmatrix.com](https://squashmatrix.com) # API Aside from the documentation provided below, there is also a `{json:api}` available and can be accessed in the same manner, with the addition of the accept header `{accept: application/vnd.api+json}`. More information about json api can be viewed on their website at [http://jsonapi.org/](http://jsonapi.org/) # Squash Matrix Scrapper There is a ruby SDK for retrieving information from [https://squashmatrix.com](https://squashmatrix.com) which can be found at https://rubygems.org/gems/squash_matrix # SDK's Please stay posted! Client sdk's for the following will be provided shortly:    - Javascript   - Java   - Ruby  # Blog Find relevent and interesting media on [wilkosz.com.au](http://wilkosz.com.au) # Contact Join this endeavor and be appart of the community [https://www.facebook.com/squashmatrixapi](https://www.facebook.com/squashmatrixapi) <hr />  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from SquashMatrixAPI.SquashMatrixClientModel.api_response_errors_errors import ApiResponseErrorsErrors  # noqa: F401,E501


class ApiResponseErrors(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'errors': 'list[ApiResponseErrorsErrors]'
    }

    attribute_map = {
        'errors': 'errors'
    }

    def __init__(self, errors=None):  # noqa: E501
        """ApiResponseErrors - a model defined in Swagger"""  # noqa: E501

        self._errors = None
        self.discriminator = None

        if errors is not None:
            self.errors = errors

    @property
    def errors(self):
        """Gets the errors of this ApiResponseErrors.  # noqa: E501


        :return: The errors of this ApiResponseErrors.  # noqa: E501
        :rtype: list[ApiResponseErrorsErrors]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this ApiResponseErrors.


        :param errors: The errors of this ApiResponseErrors.  # noqa: E501
        :type: list[ApiResponseErrorsErrors]
        """

        self._errors = errors

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiResponseErrors):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
