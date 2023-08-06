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

class DeleteNotesSlideParagraphRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteNotesSlideParagraphsRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, paragraphs = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.paragraphs = paragraphs
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteNotesSlidePortionRequest(object):

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

class DeleteNotesSlidePortionsRequest(object):

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

class DeleteNotesSlideShapeRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteNotesSlideShapesRequest(object):

    def __init__(self, name, slide_index, path = None, shapes = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.path = path
        self.shapes = shapes
        self.password = password
        self.folder = folder
        self.storage = storage

class GetNotesSlideShapeRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetNotesSlideShapeParagraphRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetNotesSlideShapeParagraphsRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetNotesSlideShapePortionRequest(object):

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

class GetNotesSlideShapePortionsRequest(object):

    def __init__(self, name, slide_index, shape_index, paragraph_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.paragraph_index = paragraph_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class GetNotesSlideShapeWithFormatRequest(object):

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

class GetNotesSlideShapesRequest(object):

    def __init__(self, name, slide_index, path = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.path = path
        self.password = password
        self.folder = folder
        self.storage = storage

class PostNotesSlideAddNewParagraphRequest(object):

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

class PostNotesSlideAddNewPortionRequest(object):

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

class PostNotesSlideAddNewShapeRequest(object):

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

class PostNotesSlideShapeSaveAsRequest(object):

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

class PutUpdateNotesSlideShapeRequest(object):

    def __init__(self, name, slide_index, shape_index, path = None, dto = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.shape_index = shape_index
        self.path = path
        self.dto = dto
        self.password = password
        self.folder = folder
        self.storage = storage

class PutUpdateNotesSlideShapeParagraphRequest(object):

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

class PutUpdateNotesSlideShapePortionRequest(object):

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

