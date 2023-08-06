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


class ChartType(object):

    """
    allowed enum values
    """
    CLUSTEREDCOLUMN = "ClusteredColumn"
    STACKEDCOLUMN = "StackedColumn"
    PERCENTSSTACKEDCOLUMN = "PercentsStackedColumn"
    CLUSTEREDCOLUMN3D = "ClusteredColumn3D"
    STACKEDCOLUMN3D = "StackedColumn3D"
    PERCENTSSTACKEDCOLUMN3D = "PercentsStackedColumn3D"
    COLUMN3D = "Column3D"
    CLUSTEREDCYLINDER = "ClusteredCylinder"
    STACKEDCYLINDER = "StackedCylinder"
    PERCENTSSTACKEDCYLINDER = "PercentsStackedCylinder"
    CYLINDER3D = "Cylinder3D"
    CLUSTEREDCONE = "ClusteredCone"
    STACKEDCONE = "StackedCone"
    PERCENTSSTACKEDCONE = "PercentsStackedCone"
    CONE3D = "Cone3D"
    CLUSTEREDPYRAMID = "ClusteredPyramid"
    STACKEDPYRAMID = "StackedPyramid"
    PERCENTSSTACKEDPYRAMID = "PercentsStackedPyramid"
    PYRAMID3D = "Pyramid3D"
    LINE = "Line"
    STACKEDLINE = "StackedLine"
    PERCENTSSTACKEDLINE = "PercentsStackedLine"
    LINEWITHMARKERS = "LineWithMarkers"
    STACKEDLINEWITHMARKERS = "StackedLineWithMarkers"
    PERCENTSSTACKEDLINEWITHMARKERS = "PercentsStackedLineWithMarkers"
    LINE3D = "Line3D"
    PIE = "Pie"
    PIE3D = "Pie3D"
    PIEOFPIE = "PieOfPie"
    EXPLODEDPIE = "ExplodedPie"
    EXPLODEDPIE3D = "ExplodedPie3D"
    BAROFPIE = "BarOfPie"
    PERCENTSSTACKEDBAR = "PercentsStackedBar"
    CLUSTEREDBAR3D = "ClusteredBar3D"
    CLUSTEREDBAR = "ClusteredBar"
    STACKEDBAR = "StackedBar"
    STACKEDBAR3D = "StackedBar3D"
    PERCENTSSTACKEDBAR3D = "PercentsStackedBar3D"
    CLUSTEREDHORIZONTALCYLINDER = "ClusteredHorizontalCylinder"
    STACKEDHORIZONTALCYLINDER = "StackedHorizontalCylinder"
    PERCENTSSTACKEDHORIZONTALCYLINDER = "PercentsStackedHorizontalCylinder"
    CLUSTEREDHORIZONTALCONE = "ClusteredHorizontalCone"
    STACKEDHORIZONTALCONE = "StackedHorizontalCone"
    PERCENTSSTACKEDHORIZONTALCONE = "PercentsStackedHorizontalCone"
    CLUSTEREDHORIZONTALPYRAMID = "ClusteredHorizontalPyramid"
    STACKEDHORIZONTALPYRAMID = "StackedHorizontalPyramid"
    PERCENTSSTACKEDHORIZONTALPYRAMID = "PercentsStackedHorizontalPyramid"
    AREA = "Area"
    STACKEDAREA = "StackedArea"
    PERCENTSSTACKEDAREA = "PercentsStackedArea"
    AREA3D = "Area3D"
    STACKEDAREA3D = "StackedArea3D"
    PERCENTSSTACKEDAREA3D = "PercentsStackedArea3D"
    SCATTERWITHMARKERS = "ScatterWithMarkers"
    SCATTERWITHSMOOTHLINESANDMARKERS = "ScatterWithSmoothLinesAndMarkers"
    SCATTERWITHSMOOTHLINES = "ScatterWithSmoothLines"
    SCATTERWITHSTRAIGHTLINESANDMARKERS = "ScatterWithStraightLinesAndMarkers"
    SCATTERWITHSTRAIGHTLINES = "ScatterWithStraightLines"
    HIGHLOWCLOSE = "HighLowClose"
    OPENHIGHLOWCLOSE = "OpenHighLowClose"
    VOLUMEHIGHLOWCLOSE = "VolumeHighLowClose"
    VOLUMEOPENHIGHLOWCLOSE = "VolumeOpenHighLowClose"
    SURFACE3D = "Surface3D"
    WIREFRAMESURFACE3D = "WireframeSurface3D"
    CONTOUR = "Contour"
    WIREFRAMECONTOUR = "WireframeContour"
    DOUGHNUT = "Doughnut"
    EXPLODEDDOUGHNUT = "ExplodedDoughnut"
    BUBBLE = "Bubble"
    BUBBLEWITH3D = "BubbleWith3D"
    RADAR = "Radar"
    RADARWITHMARKERS = "RadarWithMarkers"
    FILLEDRADAR = "FilledRadar"
    SERIESOFMIXEDTYPES = "SeriesOfMixedTypes"

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
        """ChartType - a model defined in Swagger"""  # noqa: E501

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
        if not isinstance(other, ChartType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
