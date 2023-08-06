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

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from asposeslidescloud.apis.api_base import ApiBase
from asposeslidescloud.api_client import ApiClient

class DocumentApi(ApiBase):

    def __init__(self, configuration = None, app_sid = None, app_key = None):
        super(DocumentApi, self).__init__(configuration, app_sid, app_key)

    def get_slides_api_info(self, **kwargs):  # noqa: E501
        """Get API info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_api_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        
        :return: ApiInfoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_slides_api_info_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_slides_api_info_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_slides_api_info_with_http_info(self, **kwargs):  # noqa: E501
        """Get API info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_api_info_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        
        :return: ApiInfoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_slides_api_info" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/info', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ApiInfoResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_slides_document(self, request, **kwargs):  # noqa: E501
        """Read presentation info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_document(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_documentRequest request: get_slides_document request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_slides_document_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_slides_document_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_slides_document_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read presentation info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_document_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_documentRequest request: get_slides_document request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_slides_document" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_slides_document`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='DocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_slides_document_with_format(self, request, **kwargs):  # noqa: E501
        """Export presentation to some format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_document_with_format(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_document_with_formatRequest request: get_slides_document_with_format request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_slides_document_with_format_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_slides_document_with_format_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_slides_document_with_format_with_http_info(self, request, **kwargs):  # noqa: E501
        """Export presentation to some format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_document_with_format_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_document_with_formatRequest request: get_slides_document_with_format request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_slides_document_with_format" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_slides_document_with_format`")  # noqa: E501
        # verify the required parameter 'format' is set
        if not request.format:
            raise ValueError("Missing the required parameter `request.format` when calling `get_slides_document_with_format`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['format'] = request.format  # noqa: E501

        query_params = []
        if request.jpeg_quality:
            query_params.append(('jpegQuality', request.jpeg_quality))  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.out_path:
            query_params.append(('outPath', request.out_path))  # noqa: E501
        if request.fonts_folder:
            query_params.append(('fontsFolder', request.fonts_folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/saveAs/{format}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_slides_document(self, request, **kwargs):  # noqa: E501
        """Create presentation   # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_document(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_documentRequest request: post_slides_document request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_slides_document_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_slides_document_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_slides_document_with_http_info(self, request, **kwargs):  # noqa: E501
        """Create presentation   # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_document_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_documentRequest request: post_slides_document request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_slides_document" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_slides_document`")  # noqa: E501
        # verify the required parameter 'data' is set
        if not request.data:
            raise ValueError("Missing the required parameter `request.data` when calling `post_slides_document`")  # noqa: E501
        # verify the required parameter 'template_path' is set
        if not request.template_path:
            raise ValueError("Missing the required parameter `request.template_path` when calling `post_slides_document`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.template_path:
            query_params.append(('templatePath', request.template_path))  # noqa: E501
        if request.template_storage:
            query_params.append(('templateStorage', request.template_storage))  # noqa: E501
        if request.is_image_data_embedded:
            query_params.append(('isImageDataEmbedded', request.is_image_data_embedded))  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.data:
            body_params = request.data

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='DocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_slides_pipeline(self, request, **kwargs):  # noqa: E501
        """Performs slides pipeline. Http-request contains pipeline DTO.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_pipeline(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_pipelineRequest request: post_slides_pipeline request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_slides_pipeline_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_slides_pipeline_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_slides_pipeline_with_http_info(self, request, **kwargs):  # noqa: E501
        """Performs slides pipeline. Http-request contains pipeline DTO.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_pipeline_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_pipelineRequest request: post_slides_pipeline request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_slides_pipeline" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []

        body_params = None
        if request.pipeline:
            body_params = request.pipeline

        files = None
        files = request.files

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/pipeline', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_slides_save_as(self, request, **kwargs):  # noqa: E501
        """Saves presentation with options  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_save_as(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_save_asRequest request: post_slides_save_as request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_slides_save_as_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_slides_save_as_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_slides_save_as_with_http_info(self, request, **kwargs):  # noqa: E501
        """Saves presentation with options  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_save_as_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_save_asRequest request: post_slides_save_as request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_slides_save_as" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_slides_save_as`")  # noqa: E501
        # verify the required parameter 'format' is set
        if not request.format:
            raise ValueError("Missing the required parameter `request.format` when calling `post_slides_save_as`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['format'] = request.format  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.out_path:
            query_params.append(('outPath', request.out_path))  # noqa: E501
        if request.fonts_folder:
            query_params.append(('fontsFolder', request.fonts_folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.options:
            body_params = request.options

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/saveAs/{format}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_slides_split(self, request, **kwargs):  # noqa: E501
        """Splitting presentations. Create one image per slide.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_split(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_splitRequest request: post_slides_split request object
        :return: SplitDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_slides_split_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_slides_split_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_slides_split_with_http_info(self, request, **kwargs):  # noqa: E501
        """Splitting presentations. Create one image per slide.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_slides_split_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_slides_splitRequest request: post_slides_split request object
        :return: SplitDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_slides_split" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_slides_split`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.format:
            query_params.append(('format', request.format))  # noqa: E501
        if request.width:
            query_params.append(('width', request.width))  # noqa: E501
        if request.height:
            query_params.append(('height', request.height))  # noqa: E501
        if request.to:
            query_params.append(('to', request.to))  # noqa: E501
        if request._from:
            query_params.append(('from', request._from))  # noqa: E501
        if request.dest_folder:
            query_params.append(('destFolder', request.dest_folder))  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.options:
            body_params = request.options

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/split', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='SplitDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_new_presentation(self, request, **kwargs):  # noqa: E501
        """Create presentation   # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_new_presentation(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_new_presentationRequest request: put_new_presentation request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_new_presentation_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_new_presentation_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_new_presentation_with_http_info(self, request, **kwargs):  # noqa: E501
        """Create presentation   # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_new_presentation_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_new_presentationRequest request: put_new_presentation request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_new_presentation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_new_presentation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.template_path:
            query_params.append(('templatePath', request.template_path))  # noqa: E501
        if request.template_password:
            query_params.append(('templatePassword', request.template_password))  # noqa: E501
        if request.template_storage:
            query_params.append(('templateStorage', request.template_storage))  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.stream:
            body_params = request.stream

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='DocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_slides_convert(self, request, **kwargs):  # noqa: E501
        """Convert presentation from request content to format specified.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_convert(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_convertRequest request: put_slides_convert request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_slides_convert_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_slides_convert_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_slides_convert_with_http_info(self, request, **kwargs):  # noqa: E501
        """Convert presentation from request content to format specified.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_convert_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_convertRequest request: put_slides_convert request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_slides_convert" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'format' is set
        if not request.format:
            raise ValueError("Missing the required parameter `request.format` when calling `put_slides_convert`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if request.format:
            query_params.append(('format', request.format))  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.out_path:
            query_params.append(('outPath', request.out_path))  # noqa: E501
        if request.fonts_folder:
            query_params.append(('fontsFolder', request.fonts_folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.document:
            body_params = request.document

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/convert', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_slides_document_from_html(self, request, **kwargs):  # noqa: E501
        """Create presentation document from html  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_document_from_html(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_document_from_htmlRequest request: put_slides_document_from_html request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_slides_document_from_html_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_slides_document_from_html_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_slides_document_from_html_with_http_info(self, request, **kwargs):  # noqa: E501
        """Create presentation document from html  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_document_from_html_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_document_from_htmlRequest request: put_slides_document_from_html request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_slides_document_from_html" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_slides_document_from_html`")  # noqa: E501
        # verify the required parameter 'html' is set
        if not request.html:
            raise ValueError("Missing the required parameter `request.html` when calling `put_slides_document_from_html`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.html:
            body_params = request.html

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/fromHtml', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='DocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_slides_slide_size(self, request, **kwargs):  # noqa: E501
        """Set slide size for the presentation.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_slide_size(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_slide_sizeRequest request: put_slides_slide_size request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_slides_slide_size_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_slides_slide_size_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_slides_slide_size_with_http_info(self, request, **kwargs):  # noqa: E501
        """Set slide size for the presentation.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_slides_slide_size_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_slides_slide_sizeRequest request: put_slides_slide_size request object
        :return: DocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_slides_slide_size" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_slides_slide_size`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.width:
            query_params.append(('width', request.width))  # noqa: E501
        if request.height:
            query_params.append(('height', request.height))  # noqa: E501
        if request.size_type:
            query_params.append(('sizeType', request.size_type))  # noqa: E501
        if request.scale_type:
            query_params.append(('scaleType', request.scale_type))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slidesize', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='DocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
