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

class GetSlidesDocumentRequest(object):

    def __init__(self, name, password = None, storage = None, folder = None):
        self.name = name
        self.password = password
        self.storage = storage
        self.folder = folder

class GetSlidesDocumentWithFormatRequest(object):

    def __init__(self, name, format, jpeg_quality = None, password = None, storage = None, folder = None, out_path = None, fonts_folder = None):
        self.name = name
        self.format = format
        self.jpeg_quality = jpeg_quality
        self.password = password
        self.storage = storage
        self.folder = folder
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class PostSlidesDocumentRequest(object):

    def __init__(self, name, data, template_path, template_storage = None, is_image_data_embedded = None, password = None, storage = None, folder = None):
        self.name = name
        self.data = data
        self.template_path = template_path
        self.template_storage = template_storage
        self.is_image_data_embedded = is_image_data_embedded
        self.password = password
        self.storage = storage
        self.folder = folder

class PostSlidesPipelineRequest(object):

    def __init__(self, pipeline = None, files = None):
        self.pipeline = pipeline
        self.files = files

class PostSlidesSaveAsRequest(object):

    def __init__(self, name, format, options = None, password = None, storage = None, folder = None, out_path = None, fonts_folder = None):
        self.name = name
        self.format = format
        self.options = options
        self.password = password
        self.storage = storage
        self.folder = folder
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class PostSlidesSplitRequest(object):

    def __init__(self, name, options = None, format = None, width = None, height = None, to = None, _from = None, dest_folder = None, password = None, storage = None, folder = None):
        self.name = name
        self.options = options
        self.format = format
        self.width = width
        self.height = height
        self.to = to
        self._from = _from
        self.dest_folder = dest_folder
        self.password = password
        self.storage = storage
        self.folder = folder

class PutNewPresentationRequest(object):

    def __init__(self, name, stream = None, template_path = None, template_password = None, template_storage = None, password = None, storage = None, folder = None):
        self.name = name
        self.stream = stream
        self.template_path = template_path
        self.template_password = template_password
        self.template_storage = template_storage
        self.password = password
        self.storage = storage
        self.folder = folder

class PutSlidesConvertRequest(object):

    def __init__(self, format, document = None, password = None, out_path = None, fonts_folder = None):
        self.format = format
        self.document = document
        self.password = password
        self.out_path = out_path
        self.fonts_folder = fonts_folder

class PutSlidesDocumentFromHtmlRequest(object):

    def __init__(self, name, html, password = None, storage = None, folder = None):
        self.name = name
        self.html = html
        self.password = password
        self.storage = storage
        self.folder = folder

class PutSlidesSlideSizeRequest(object):

    def __init__(self, name, password = None, storage = None, folder = None, width = None, height = None, size_type = None, scale_type = None):
        self.name = name
        self.password = password
        self.storage = storage
        self.folder = folder
        self.width = width
        self.height = height
        self.size_type = size_type
        self.scale_type = scale_type

