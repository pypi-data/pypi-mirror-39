# coding: utf-8

# flake8: noqa
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

from __future__ import absolute_import


from asposeslidescloud.models.requests.document_api_requests import GetSlidesDocumentRequest
from asposeslidescloud.models.requests.document_api_requests import GetSlidesDocumentWithFormatRequest
from asposeslidescloud.models.requests.document_api_requests import PostSlidesDocumentRequest
from asposeslidescloud.models.requests.document_api_requests import PostSlidesPipelineRequest
from asposeslidescloud.models.requests.document_api_requests import PostSlidesSaveAsRequest
from asposeslidescloud.models.requests.document_api_requests import PostSlidesSplitRequest
from asposeslidescloud.models.requests.document_api_requests import PutNewPresentationRequest
from asposeslidescloud.models.requests.document_api_requests import PutSlidesConvertRequest
from asposeslidescloud.models.requests.document_api_requests import PutSlidesDocumentFromHtmlRequest
from asposeslidescloud.models.requests.document_api_requests import PutSlidesSlideSizeRequest
from asposeslidescloud.models.requests.images_api_requests import GetSlidesImageWithFormatRequest
from asposeslidescloud.models.requests.images_api_requests import GetSlidesImagesRequest
from asposeslidescloud.models.requests.images_api_requests import GetSlidesSlideImagesRequest
from asposeslidescloud.models.requests.layout_slides_api_requests import GetLayoutSlideRequest
from asposeslidescloud.models.requests.layout_slides_api_requests import GetLayoutSlidesListRequest
from asposeslidescloud.models.requests.layout_slides_api_requests import PostCopyLayoutSlideFromSourcePresentationRequest
from asposeslidescloud.models.requests.layout_slides_api_requests import PutLayoutSlideRequest
from asposeslidescloud.models.requests.master_slides_api_requests import GetMasterSlideRequest
from asposeslidescloud.models.requests.master_slides_api_requests import GetMasterSlidesListRequest
from asposeslidescloud.models.requests.master_slides_api_requests import PostCopyMasterSlideFromSourcePresentationRequest
from asposeslidescloud.models.requests.merge_document_api_requests import PostPresentationMergeRequest
from asposeslidescloud.models.requests.merge_document_api_requests import PutPresentationMergeRequest
from asposeslidescloud.models.requests.notes_slide_api_requests import DeleteNotesSlideRequest
from asposeslidescloud.models.requests.notes_slide_api_requests import GetNotesSlideRequest
from asposeslidescloud.models.requests.notes_slide_api_requests import GetNotesSlideWithFormatRequest
from asposeslidescloud.models.requests.notes_slide_api_requests import PostAddNotesSlideRequest
from asposeslidescloud.models.requests.notes_slide_api_requests import PutUpdateNotesSlideRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlideParagraphRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlideParagraphsRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlidePortionRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlidePortionsRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlideShapeRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import DeleteNotesSlideShapesRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapeRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapeParagraphRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapeParagraphsRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapePortionRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapePortionsRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapeWithFormatRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import GetNotesSlideShapesRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PostNotesSlideAddNewParagraphRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PostNotesSlideAddNewPortionRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PostNotesSlideAddNewShapeRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PostNotesSlideShapeSaveAsRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PutUpdateNotesSlideShapeRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PutUpdateNotesSlideShapeParagraphRequest
from asposeslidescloud.models.requests.notes_slide_shapes_api_requests import PutUpdateNotesSlideShapePortionRequest
from asposeslidescloud.models.requests.placeholders_api_requests import GetSlidesPlaceholderRequest
from asposeslidescloud.models.requests.placeholders_api_requests import GetSlidesPlaceholdersRequest
from asposeslidescloud.models.requests.properties_api_requests import DeleteSlidesDocumentPropertiesRequest
from asposeslidescloud.models.requests.properties_api_requests import DeleteSlidesDocumentPropertyRequest
from asposeslidescloud.models.requests.properties_api_requests import GetSlidesDocumentPropertiesRequest
from asposeslidescloud.models.requests.properties_api_requests import GetSlidesDocumentPropertyRequest
from asposeslidescloud.models.requests.properties_api_requests import PostSlidesSetDocumentPropertiesRequest
from asposeslidescloud.models.requests.properties_api_requests import PutSlidesSetDocumentPropertyRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeleteParagraphRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeleteParagraphsRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeletePortionRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeletePortionsRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeleteSlideShapeRequest
from asposeslidescloud.models.requests.shapes_api_requests import DeleteSlideShapesRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetParagraphPortionRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetParagraphPortionsRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetShapeParagraphRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetShapeWithFormatRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetSlideShapeRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetSlideShapeParagraphsRequest
from asposeslidescloud.models.requests.shapes_api_requests import GetSlideShapesRequest
from asposeslidescloud.models.requests.shapes_api_requests import PostAddNewParagraphRequest
from asposeslidescloud.models.requests.shapes_api_requests import PostAddNewPortionRequest
from asposeslidescloud.models.requests.shapes_api_requests import PostAddNewShapeRequest
from asposeslidescloud.models.requests.shapes_api_requests import PostShapeSaveAsRequest
from asposeslidescloud.models.requests.shapes_api_requests import PutSetParagraphPortionPropertiesRequest
from asposeslidescloud.models.requests.shapes_api_requests import PutSetParagraphPropertiesRequest
from asposeslidescloud.models.requests.shapes_api_requests import PutSlideShapeInfoRequest
from asposeslidescloud.models.requests.slides_api_requests import DeleteSlideByIndexRequest
from asposeslidescloud.models.requests.slides_api_requests import DeleteSlidesCleanSlidesListRequest
from asposeslidescloud.models.requests.slides_api_requests import DeleteSlidesSlideBackgroundRequest
from asposeslidescloud.models.requests.slides_api_requests import GetSlideWithFormatRequest
from asposeslidescloud.models.requests.slides_api_requests import GetSlidesSlideRequest
from asposeslidescloud.models.requests.slides_api_requests import GetSlidesSlideBackgroundRequest
from asposeslidescloud.models.requests.slides_api_requests import GetSlidesSlideCommentsRequest
from asposeslidescloud.models.requests.slides_api_requests import GetSlidesSlidesListRequest
from asposeslidescloud.models.requests.slides_api_requests import PostSlideSaveAsRequest
from asposeslidescloud.models.requests.slides_api_requests import PostSlidesReorderPositionRequest
from asposeslidescloud.models.requests.slides_api_requests import PutSlidesSlideRequest
from asposeslidescloud.models.requests.slides_api_requests import PutSlidesSlideBackgroundRequest
from asposeslidescloud.models.requests.text_api_requests import GetSlidesPresentationTextItemsRequest
from asposeslidescloud.models.requests.text_api_requests import GetSlidesSlideTextItemsRequest
from asposeslidescloud.models.requests.text_api_requests import PostSlidesPresentationReplaceTextRequest
from asposeslidescloud.models.requests.text_api_requests import PostSlidesSlideReplaceTextRequest
from asposeslidescloud.models.requests.theme_api_requests import GetSlidesThemeRequest
from asposeslidescloud.models.requests.theme_api_requests import GetSlidesThemeColorSchemeRequest
from asposeslidescloud.models.requests.theme_api_requests import GetSlidesThemeFontSchemeRequest
from asposeslidescloud.models.requests.theme_api_requests import GetSlidesThemeFormatSchemeRequest
