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

class DeleteSlideByIndexRequest(object):

    def __init__(self, name, slide_index, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteSlidesCleanSlidesListRequest(object):

    def __init__(self, name, slides = None, password = None, folder = None, storage = None):
        self.name = name
        self.slides = slides
        self.password = password
        self.folder = folder
        self.storage = storage

class DeleteSlidesSlideBackgroundRequest(object):

    def __init__(self, name, slide_index, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlideWithFormatRequest(object):

    def __init__(self, name, slide_index, format, width = None, height = None, password = None, folder = None, storage = None, out_path = None, fonts_folder = None):
        self.name = name
        self.slide_index = slide_index
        self.format = format
        self.width = width
        self.height = height
        self.password = password
        self.folder = folder
        self.storage = storage
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class GetSlidesSlideRequest(object):

    def __init__(self, name, slide_index, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlidesSlideBackgroundRequest(object):

    def __init__(self, name, slide_index, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlidesSlideCommentsRequest(object):

    def __init__(self, name, slide_index, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.password = password
        self.folder = folder
        self.storage = storage

class GetSlidesSlidesListRequest(object):

    def __init__(self, name, password = None, folder = None, storage = None):
        self.name = name
        self.password = password
        self.folder = folder
        self.storage = storage

class PostSlideSaveAsRequest(object):

    def __init__(self, name, slide_index, format, options = None, width = None, height = None, password = None, folder = None, storage = None, out_path = None, fonts_folder = None):
        self.name = name
        self.slide_index = slide_index
        self.format = format
        self.options = options
        self.width = width
        self.height = height
        self.password = password
        self.folder = folder
        self.storage = storage
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class PostSlidesReorderPositionRequest(object):

    def __init__(self, name, old_position = None, new_position = None, slide_to_copy = None, position = None, slide_to_clone = None, source = None, password = None, folder = None, storage = None, layout_alias = None):
        self.name = name
        self.old_position = old_position
        self.new_position = new_position
        self.slide_to_copy = slide_to_copy
        self.position = position
        self.slide_to_clone = slide_to_clone
        self.source = source
        self.password = password
        self.folder = folder
        self.storage = storage
        self.layout_alias = layout_alias

class PutSlidesSlideRequest(object):

    def __init__(self, name, slide_index, slide_dto = None, password = None, folder = None, storage = None):
        self.name = name
        self.slide_index = slide_index
        self.slide_dto = slide_dto
        self.password = password
        self.folder = folder
        self.storage = storage

class PutSlidesSlideBackgroundRequest(object):

    def __init__(self, name, slide_index, background = None, folder = None, password = None, storage = None, color = None):
        self.name = name
        self.slide_index = slide_index
        self.background = background
        self.folder = folder
        self.password = password
        self.storage = storage
        self.color = color

