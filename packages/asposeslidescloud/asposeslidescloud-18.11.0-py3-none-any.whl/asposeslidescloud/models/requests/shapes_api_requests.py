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

from __future__ import absolute_import

class DeleteParagraphRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteParagraphsRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, paragraphs = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.paragraphs = paragraphs
        self.password = password
        self.folder = folder
        self.storage = storage

class DeletePortionRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, portion_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.portion_index = portion_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class DeletePortionsRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, portions = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.portions = portions
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteSlideShapeRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteSlideShapesRequest(object):

    def __init__(self, name, slide_index, path = None, shapes = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.path = path
        self.shapes = shapes
        self.password = password
        self.folder = folder
        self.storage = storage

class GetParagraphPortionRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, portion_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.portion_index = portion_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetParagraphPortionsRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetShapeParagraphRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetShapeWithFormatRequest(object):

    def __init__(self, name, slide_index, shape_index, format, password = None, folder = None, storage = None, scale_x = None, scale_y = None, bounds = None, out_path = None, fonts_folder = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.format = format
        self.password = password
        self.folder = folder
        self.storage = storage
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.bounds = bounds
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class GetSlideShapeRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlideShapeParagraphsRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlideShapesRequest(object):

    def __init__(self, name, slide_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class PostAddNewParagraphRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, dto = None, password = None, folder = None, storage = None, position = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage
        self.position = position

class PostAddNewPortionRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, dto = None, password = None, folder = None, storage = None, position = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage
        self.position = position

class PostAddNewShapeRequest(object):

    def __init__(self, name, slide_index, path = None, dto = None, password = None, folder = None, storage = None, shape_to_clone = None, position = None):
        self.name = name
        self.slide_index = slide_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage
        self.shape_to_clone = shape_to_clone
        self.position = position

class PostShapeSaveAsRequest(object):

    def __init__(self, name, slide_index, shape_index, format, options = None, password = None, folder = None, storage = None, scale_x = None, scale_y = None, bounds = None, out_path = None, fonts_folder = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.format = format
        self.options = options
        self.password = password
        self.folder = folder
        self.storage = storage
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.bounds = bounds
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class PutSetParagraphPortionPropertiesRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, portion_index, path = None, dto = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.portion_index = portion_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage

class PutSetParagraphPropertiesRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, dto = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage

class PutSlideShapeInfoRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, dto = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage

