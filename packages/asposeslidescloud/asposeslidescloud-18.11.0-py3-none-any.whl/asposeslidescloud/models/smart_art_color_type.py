# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose">
#   Copyright (c) 2018 Aspose.Slides for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six


class SmartArtColorType(object):

    """
    allowed enum values
    """
    DARK1OUTLINE = "Dark1Outline"
    DARK2OUTLINE = "Dark2Outline"
    DARKFILL = "DarkFill"
    COLORFULACCENTCOLORS = "ColorfulAccentColors"
    COLORFULACCENTCOLORS2TO3 = "ColorfulAccentColors2to3"
    COLORFULACCENTCOLORS3TO4 = "ColorfulAccentColors3to4"
    COLORFULACCENTCOLORS4TO5 = "ColorfulAccentColors4to5"
    COLORFULACCENTCOLORS5TO6 = "ColorfulAccentColors5to6"
    COLOREDOUTLINEACCENT1 = "ColoredOutlineAccent1"
    COLOREDFILLACCENT1 = "ColoredFillAccent1"
    GRADIENTRANGEACCENT1 = "GradientRangeAccent1"
    GRADIENTLOOPACCENT1 = "GradientLoopAccent1"
    TRANSPARENTGRADIENTRANGEACCENT1 = "TransparentGradientRangeAccent1"
    COLOREDOUTLINEACCENT2 = "ColoredOutlineAccent2"
    COLOREDFILLACCENT2 = "ColoredFillAccent2"
    GRADIENTRANGEACCENT2 = "GradientRangeAccent2"
    GRADIENTLOOPACCENT2 = "GradientLoopAccent2"
    TRANSPARENTGRADIENTRANGEACCENT2 = "TransparentGradientRangeAccent2"
    COLOREDOUTLINEACCENT3 = "ColoredOutlineAccent3"
    COLOREDFILLACCENT3 = "ColoredFillAccent3"
    GRADIENTRANGEACCENT3 = "GradientRangeAccent3"
    GRADIENTLOOPACCENT3 = "GradientLoopAccent3"
    TRANSPARENTGRADIENTRANGEACCENT3 = "TransparentGradientRangeAccent3"
    COLOREDOUTLINEACCENT4 = "ColoredOutlineAccent4"
    COLOREDFILLACCENT4 = "ColoredFillAccent4"
    GRADIENTRANGEACCENT4 = "GradientRangeAccent4"
    GRADIENTLOOPACCENT4 = "GradientLoopAccent4"
    TRANSPARENTGRADIENTRANGEACCENT4 = "TransparentGradientRangeAccent4"
    COLOREDOUTLINEACCENT5 = "ColoredOutlineAccent5"
    COLOREDFILLACCENT5 = "ColoredFillAccent5"
    GRADIENTRANGEACCENT5 = "GradientRangeAccent5"
    GRADIENTLOOPACCENT5 = "GradientLoopAccent5"
    TRANSPARENTGRADIENTRANGEACCENT5 = "TransparentGradientRangeAccent5"
    COLOREDOUTLINEACCENT6 = "ColoredOutlineAccent6"
    COLOREDFILLACCENT6 = "ColoredFillAccent6"
    GRADIENTRANGEACCENT6 = "GradientRangeAccent6"
    GRADIENTLOOPACCENT6 = "GradientLoopAccent6"
    TRANSPARENTGRADIENTRANGEACCENT6 = "TransparentGradientRangeAccent6"

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
    }

    attribute_map = {
    }

    def __init__(self):  # noqa: E501
        """SmartArtColorType - a model defined in Swagger"""  # noqa: E501

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
        if not isinstance(other, SmartArtColorType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
