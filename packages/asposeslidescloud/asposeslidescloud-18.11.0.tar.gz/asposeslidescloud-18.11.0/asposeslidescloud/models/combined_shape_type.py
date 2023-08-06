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


class CombinedShapeType(object):

    """
    allowed enum values
    """
    CUSTOM = "Custom"
    LINE = "Line"
    LINEINVERSE = "LineInverse"
    TRIANGLE = "Triangle"
    RIGHTTRIANGLE = "RightTriangle"
    RECTANGLE = "Rectangle"
    DIAMOND = "Diamond"
    PARALLELOGRAM = "Parallelogram"
    TRAPEZOID = "Trapezoid"
    NONISOSCELESTRAPEZOID = "NonIsoscelesTrapezoid"
    PENTAGON = "Pentagon"
    HEXAGON = "Hexagon"
    HEPTAGON = "Heptagon"
    OCTAGON = "Octagon"
    DECAGON = "Decagon"
    DODECAGON = "Dodecagon"
    FOURPOINTEDSTAR = "FourPointedStar"
    FIVEPOINTEDSTAR = "FivePointedStar"
    SIXPOINTEDSTAR = "SixPointedStar"
    SEVENPOINTEDSTAR = "SevenPointedStar"
    EIGHTPOINTEDSTAR = "EightPointedStar"
    TENPOINTEDSTAR = "TenPointedStar"
    TWELVEPOINTEDSTAR = "TwelvePointedStar"
    SIXTEENPOINTEDSTAR = "SixteenPointedStar"
    TWENTYFOURPOINTEDSTAR = "TwentyFourPointedStar"
    THIRTYTWOPOINTEDSTAR = "ThirtyTwoPointedStar"
    ROUNDCORNERRECTANGLE = "RoundCornerRectangle"
    ONEROUNDCORNERRECTANGLE = "OneRoundCornerRectangle"
    TWOSAMESIDEROUNDCORNERRECTANGLE = "TwoSamesideRoundCornerRectangle"
    TWODIAGONALROUNDCORNERRECTANGLE = "TwoDiagonalRoundCornerRectangle"
    ONESNIPONEROUNDCORNERRECTANGLE = "OneSnipOneRoundCornerRectangle"
    ONESNIPCORNERRECTANGLE = "OneSnipCornerRectangle"
    TWOSAMESIDESNIPCORNERRECTANGLE = "TwoSamesideSnipCornerRectangle"
    TWODIAGONALSNIPCORNERRECTANGLE = "TwoDiagonalSnipCornerRectangle"
    PLAQUE = "Plaque"
    ELLIPSE = "Ellipse"
    TEARDROP = "Teardrop"
    HOMEPLATE = "HomePlate"
    CHEVRON = "Chevron"
    PIEWEDGE = "PieWedge"
    PIE = "Pie"
    BLOCKARC = "BlockArc"
    DONUT = "Donut"
    NOSMOKING = "NoSmoking"
    RIGHTARROW = "RightArrow"
    LEFTARROW = "LeftArrow"
    UPARROW = "UpArrow"
    DOWNARROW = "DownArrow"
    STRIPEDRIGHTARROW = "StripedRightArrow"
    NOTCHEDRIGHTARROW = "NotchedRightArrow"
    BENTUPARROW = "BentUpArrow"
    LEFTRIGHTARROW = "LeftRightArrow"
    UPDOWNARROW = "UpDownArrow"
    LEFTUPARROW = "LeftUpArrow"
    LEFTRIGHTUPARROW = "LeftRightUpArrow"
    QUADARROW = "QuadArrow"
    CALLOUTLEFTARROW = "CalloutLeftArrow"
    CALLOUTRIGHTARROW = "CalloutRightArrow"
    CALLOUTUPARROW = "CalloutUpArrow"
    CALLOUTDOWNARROW = "CalloutDownArrow"
    CALLOUTLEFTRIGHTARROW = "CalloutLeftRightArrow"
    CALLOUTUPDOWNARROW = "CalloutUpDownArrow"
    CALLOUTQUADARROW = "CalloutQuadArrow"
    BENTARROW = "BentArrow"
    UTURNARROW = "UTurnArrow"
    CIRCULARARROW = "CircularArrow"
    LEFTCIRCULARARROW = "LeftCircularArrow"
    LEFTRIGHTCIRCULARARROW = "LeftRightCircularArrow"
    CURVEDRIGHTARROW = "CurvedRightArrow"
    CURVEDLEFTARROW = "CurvedLeftArrow"
    CURVEDUPARROW = "CurvedUpArrow"
    CURVEDDOWNARROW = "CurvedDownArrow"
    SWOOSHARROW = "SwooshArrow"
    CUBE = "Cube"
    CAN = "Can"
    LIGHTNINGBOLT = "LightningBolt"
    HEART = "Heart"
    SUN = "Sun"
    MOON = "Moon"
    SMILEYFACE = "SmileyFace"
    IRREGULARSEAL1 = "IrregularSeal1"
    IRREGULARSEAL2 = "IrregularSeal2"
    FOLDEDCORNER = "FoldedCorner"
    BEVEL = "Bevel"
    FRAME = "Frame"
    HALFFRAME = "HalfFrame"
    CORNER = "Corner"
    DIAGONALSTRIPE = "DiagonalStripe"
    CHORD = "Chord"
    CURVEDARC = "CurvedArc"
    LEFTBRACKET = "LeftBracket"
    RIGHTBRACKET = "RightBracket"
    LEFTBRACE = "LeftBrace"
    RIGHTBRACE = "RightBrace"
    BRACKETPAIR = "BracketPair"
    BRACEPAIR = "BracePair"
    STRAIGHTCONNECTOR1 = "StraightConnector1"
    BENTCONNECTOR2 = "BentConnector2"
    BENTCONNECTOR3 = "BentConnector3"
    BENTCONNECTOR4 = "BentConnector4"
    BENTCONNECTOR5 = "BentConnector5"
    CURVEDCONNECTOR2 = "CurvedConnector2"
    CURVEDCONNECTOR3 = "CurvedConnector3"
    CURVEDCONNECTOR4 = "CurvedConnector4"
    CURVEDCONNECTOR5 = "CurvedConnector5"
    CALLOUT1 = "Callout1"
    CALLOUT2 = "Callout2"
    CALLOUT3 = "Callout3"
    CALLOUT1WITHACCENT = "Callout1WithAccent"
    CALLOUT2WITHACCENT = "Callout2WithAccent"
    CALLOUT3WITHACCENT = "Callout3WithAccent"
    CALLOUT1WITHBORDER = "Callout1WithBorder"
    CALLOUT2WITHBORDER = "Callout2WithBorder"
    CALLOUT3WITHBORDER = "Callout3WithBorder"
    CALLOUT1WITHBORDERANDACCENT = "Callout1WithBorderAndAccent"
    CALLOUT2WITHBORDERANDACCENT = "Callout2WithBorderAndAccent"
    CALLOUT3WITHBORDERANDACCENT = "Callout3WithBorderAndAccent"
    CALLOUTWEDGERECTANGLE = "CalloutWedgeRectangle"
    CALLOUTWEDGEROUNDRECTANGLE = "CalloutWedgeRoundRectangle"
    CALLOUTWEDGEELLIPSE = "CalloutWedgeEllipse"
    CALLOUTCLOUD = "CalloutCloud"
    CLOUD = "Cloud"
    RIBBON = "Ribbon"
    RIBBON2 = "Ribbon2"
    ELLIPSERIBBON = "EllipseRibbon"
    ELLIPSERIBBON2 = "EllipseRibbon2"
    LEFTRIGHTRIBBON = "LeftRightRibbon"
    VERTICALSCROLL = "VerticalScroll"
    HORIZONTALSCROLL = "HorizontalScroll"
    WAVE = "Wave"
    DOUBLEWAVE = "DoubleWave"
    PLUS = "Plus"
    PROCESSFLOW = "ProcessFlow"
    DECISIONFLOW = "DecisionFlow"
    INPUTOUTPUTFLOW = "InputOutputFlow"
    PREDEFINEDPROCESSFLOW = "PredefinedProcessFlow"
    INTERNALSTORAGEFLOW = "InternalStorageFlow"
    DOCUMENTFLOW = "DocumentFlow"
    MULTIDOCUMENTFLOW = "MultiDocumentFlow"
    TERMINATORFLOW = "TerminatorFlow"
    PREPARATIONFLOW = "PreparationFlow"
    MANUALINPUTFLOW = "ManualInputFlow"
    MANUALOPERATIONFLOW = "ManualOperationFlow"
    CONNECTORFLOW = "ConnectorFlow"
    PUNCHEDCARDFLOW = "PunchedCardFlow"
    PUNCHEDTAPEFLOW = "PunchedTapeFlow"
    SUMMINGJUNCTIONFLOW = "SummingJunctionFlow"
    ORFLOW = "OrFlow"
    COLLATEFLOW = "CollateFlow"
    SORTFLOW = "SortFlow"
    EXTRACTFLOW = "ExtractFlow"
    MERGEFLOW = "MergeFlow"
    OFFLINESTORAGEFLOW = "OfflineStorageFlow"
    ONLINESTORAGEFLOW = "OnlineStorageFlow"
    MAGNETICTAPEFLOW = "MagneticTapeFlow"
    MAGNETICDISKFLOW = "MagneticDiskFlow"
    MAGNETICDRUMFLOW = "MagneticDrumFlow"
    DISPLAYFLOW = "DisplayFlow"
    DELAYFLOW = "DelayFlow"
    ALTERNATEPROCESSFLOW = "AlternateProcessFlow"
    OFFPAGECONNECTORFLOW = "OffPageConnectorFlow"
    BLANKBUTTON = "BlankButton"
    HOMEBUTTON = "HomeButton"
    HELPBUTTON = "HelpButton"
    INFORMATIONBUTTON = "InformationButton"
    FORWARDORNEXTBUTTON = "ForwardOrNextButton"
    BACKORPREVIOUSBUTTON = "BackOrPreviousButton"
    ENDBUTTON = "EndButton"
    BEGINNINGBUTTON = "BeginningButton"
    RETURNBUTTON = "ReturnButton"
    DOCUMENTBUTTON = "DocumentButton"
    SOUNDBUTTON = "SoundButton"
    MOVIEBUTTON = "MovieButton"
    GEAR6 = "Gear6"
    GEAR9 = "Gear9"
    FUNNEL = "Funnel"
    PLUSMATH = "PlusMath"
    MINUSMATH = "MinusMath"
    MULTIPLYMATH = "MultiplyMath"
    DIVIDEMATH = "DivideMath"
    EQUALMATH = "EqualMath"
    NOTEQUALMATH = "NotEqualMath"
    CORNERTABS = "CornerTabs"
    SQUARETABS = "SquareTabs"
    PLAQUETABS = "PlaqueTabs"
    CHARTX = "ChartX"
    CHARTSTAR = "ChartStar"
    CHARTPLUS = "ChartPlus"
    CHART = "Chart"
    TABLE = "Table"
    PICTUREFRAME = "PictureFrame"
    VIDEOFRAME = "VideoFrame"
    AUDIOFRAME = "AudioFrame"
    DIAGRAM = "Diagram"
    OLEOBJECTFRAME = "OleObjectFrame"
    GROUPSHAPE = "GroupShape"
    GRAPHICALOBJECT = "GraphicalObject"
    NOTDEFINED = "NotDefined"

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
        """CombinedShapeType - a model defined in Swagger"""  # noqa: E501

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
        if not isinstance(other, CombinedShapeType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
