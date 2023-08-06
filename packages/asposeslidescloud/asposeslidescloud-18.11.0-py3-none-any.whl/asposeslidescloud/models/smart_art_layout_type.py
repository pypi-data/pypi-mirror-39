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


class SmartArtLayoutType(object):

    """
    allowed enum values
    """
    ACCENTPROCESS = "AccentProcess"
    ACCENTEDPICTURE = "AccentedPicture"
    ALTERNATINGFLOW = "AlternatingFlow"
    ALTERNATINGHEXAGONS = "AlternatingHexagons"
    ALTERNATINGPICTUREBLOCKS = "AlternatingPictureBlocks"
    ALTERNATINGPICTURECIRCLES = "AlternatingPictureCircles"
    ARROWRIBBON = "ArrowRibbon"
    ASCENDINGPICTUREACCENTPROCESS = "AscendingPictureAccentProcess"
    BALANCE = "Balance"
    BASICBENDINGPROCESS = "BasicBendingProcess"
    BASICBLOCKLIST = "BasicBlockList"
    BASICCHEVRONPROCESS = "BasicChevronProcess"
    BASICCYCLE = "BasicCycle"
    BASICMATRIX = "BasicMatrix"
    BASICPIE = "BasicPie"
    BASICPROCESS = "BasicProcess"
    BASICPYRAMID = "BasicPyramid"
    BASICRADIAL = "BasicRadial"
    BASICTARGET = "BasicTarget"
    BASICTIMELINE = "BasicTimeline"
    BASICVENN = "BasicVenn"
    BENDINGPICTUREACCENTLIST = "BendingPictureAccentList"
    BENDINGPICTUREBLOCKS = "BendingPictureBlocks"
    BENDINGPICTURECAPTION = "BendingPictureCaption"
    BENDINGPICTURECAPTIONLIST = "BendingPictureCaptionList"
    BENDINGPICTURESEMITRANSPARENTTEXT = "BendingPictureSemiTransparentText"
    BLOCKCYCLE = "BlockCycle"
    BUBBLEPICTURELIST = "BubblePictureList"
    CAPTIONEDPICTURES = "CaptionedPictures"
    CHEVRONLIST = "ChevronList"
    CIRCLEACCENTTIMELINE = "CircleAccentTimeline"
    CIRCLEARROWPROCESS = "CircleArrowProcess"
    CIRCLEPICTUREHIERARCHY = "CirclePictureHierarchy"
    CIRCLERELATIONSHIP = "CircleRelationship"
    CIRCULARBENDINGPROCESS = "CircularBendingProcess"
    CIRCULARPICTURECALLOUT = "CircularPictureCallout"
    CLOSEDCHEVRONPROCESS = "ClosedChevronProcess"
    CONTINUOUSARROWPROCESS = "ContinuousArrowProcess"
    CONTINUOUSBLOCKPROCESS = "ContinuousBlockProcess"
    CONTINUOUSCYCLE = "ContinuousCycle"
    CONTINUOUSPICTURELIST = "ContinuousPictureList"
    CONVERGINGARROWS = "ConvergingArrows"
    CONVERGINGRADIAL = "ConvergingRadial"
    COUNTERBALANCEARROWS = "CounterbalanceArrows"
    CYCLEMATRIX = "CycleMatrix"
    DESCENDINGBLOCKLIST = "DescendingBlockList"
    DESCENDINGPROCESS = "DescendingProcess"
    DETAILEDPROCESS = "DetailedProcess"
    DIVERGINGARROWS = "DivergingArrows"
    DIVERGINGRADIAL = "DivergingRadial"
    EQUATION = "Equation"
    FRAMEDTEXTPICTURE = "FramedTextPicture"
    FUNNEL = "Funnel"
    GEAR = "Gear"
    GRIDMATRIX = "GridMatrix"
    GROUPEDLIST = "GroupedList"
    HALFCIRCLEORGANIZATIONCHART = "HalfCircleOrganizationChart"
    HEXAGONCLUSTER = "HexagonCluster"
    HIERARCHY = "Hierarchy"
    HIERARCHYLIST = "HierarchyList"
    HORIZONTALBULLETLIST = "HorizontalBulletList"
    HORIZONTALHIERARCHY = "HorizontalHierarchy"
    HORIZONTALLABELEDHIERARCHY = "HorizontalLabeledHierarchy"
    HORIZONTALMULTILEVELHIERARCHY = "HorizontalMultiLevelHierarchy"
    HORIZONTALORGANIZATIONCHART = "HorizontalOrganizationChart"
    HORIZONTALPICTURELIST = "HorizontalPictureList"
    INCREASINGARROWSPROCESS = "IncreasingArrowsProcess"
    INCREASINGCIRCLEPROCESS = "IncreasingCircleProcess"
    INVERTEDPYRAMID = "InvertedPyramid"
    LABELEDHIERARCHY = "LabeledHierarchy"
    LINEARVENN = "LinearVenn"
    LINEDLIST = "LinedList"
    MULTIDIRECTIONALCYCLE = "MultidirectionalCycle"
    NAMEANDTITLEORGANIZATIONCHART = "NameandTitleOrganizationChart"
    NESTEDTARGET = "NestedTarget"
    NONDIRECTIONALCYCLE = "NondirectionalCycle"
    OPPOSINGARROWS = "OpposingArrows"
    OPPOSINGIDEAS = "OpposingIdeas"
    ORGANIZATIONCHART = "OrganizationChart"
    PHASEDPROCESS = "PhasedProcess"
    PICTUREACCENTBLOCKS = "PictureAccentBlocks"
    PICTUREACCENTLIST = "PictureAccentList"
    PICTUREACCENTPROCESS = "PictureAccentProcess"
    PICTURECAPTIONLIST = "PictureCaptionList"
    PICTUREGRID = "PictureGrid"
    PICTURELINEUP = "PictureLineup"
    PICTURESTRIPS = "PictureStrips"
    PIEPROCESS = "PieProcess"
    PLUSANDMINUS = "PlusandMinus"
    PROCESSARROWS = "ProcessArrows"
    PROCESSLIST = "ProcessList"
    PYRAMIDLIST = "PyramidList"
    RADIALCLUSTER = "RadialCluster"
    RADIALCYCLE = "RadialCycle"
    RADIALLIST = "RadialList"
    RADIALVENN = "RadialVenn"
    RANDOMTORESULTPROCESS = "RandomToResultProcess"
    REPEATINGBENDINGPROCESS = "RepeatingBendingProcess"
    REVERSELIST = "ReverseList"
    SEGMENTEDCYCLE = "SegmentedCycle"
    SEGMENTEDPROCESS = "SegmentedProcess"
    SEGMENTEDPYRAMID = "SegmentedPyramid"
    SNAPSHOTPICTURELIST = "SnapshotPictureList"
    SPIRALPICTURE = "SpiralPicture"
    SQUAREACCENTLIST = "SquareAccentList"
    STACKEDLIST = "StackedList"
    STACKEDVENN = "StackedVenn"
    STAGGEREDPROCESS = "StaggeredProcess"
    STEPDOWNPROCESS = "StepDownProcess"
    STEPUPPROCESS = "StepUpProcess"
    SUBSTEPPROCESS = "SubStepProcess"
    TABLEHIERARCHY = "TableHierarchy"
    TABLELIST = "TableList"
    TARGETLIST = "TargetList"
    TEXTCYCLE = "TextCycle"
    TITLEPICTURELINEUP = "TitlePictureLineup"
    TITLEDMATRIX = "TitledMatrix"
    TITLEDPICTUREACCENTLIST = "TitledPictureAccentList"
    TITLEDPICTUREBLOCKS = "TitledPictureBlocks"
    TRAPEZOIDLIST = "TrapezoidList"
    UPWARDARROW = "UpwardArrow"
    VERTICALACCENTLIST = "VerticalAccentList"
    VERTICALARROWLIST = "VerticalArrowList"
    VERTICALBENDINGPROCESS = "VerticalBendingProcess"
    VERTICALBLOCKLIST = "VerticalBlockList"
    VERTICALBOXLIST = "VerticalBoxList"
    VERTICALBULLETLIST = "VerticalBulletList"
    VERTICALCHEVRONLIST = "VerticalChevronList"
    VERTICALCIRCLELIST = "VerticalCircleList"
    VERTICALCURVEDLIST = "VerticalCurvedList"
    VERTICALEQUATION = "VerticalEquation"
    VERTICALPICTUREACCENTLIST = "VerticalPictureAccentList"
    VERTICALPICTURELIST = "VerticalPictureList"
    VERTICALPROCESS = "VerticalProcess"
    CUSTOM = "Custom"
    PICTUREORGANIZATIONCHART = "PictureOrganizationChart"

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
        """SmartArtLayoutType - a model defined in Swagger"""  # noqa: E501

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
        if not isinstance(other, SmartArtLayoutType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
