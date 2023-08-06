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

class PlaceholdersApi(ApiBase):

    def __init__(self, configuration = None, app_sid = None, app_key = None):
        super(PlaceholdersApi, self).__init__(configuration, app_sid, app_key)

    def get_slides_placeholder(self, request, **kwargs):  # noqa: E501
        """Read slide placeholder info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_placeholder(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_placeholderRequest request: get_slides_placeholder request object
        :return: PlaceholderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_slides_placeholder_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_slides_placeholder_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_slides_placeholder_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide placeholder info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_placeholder_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_placeholderRequest request: get_slides_placeholder request object
        :return: PlaceholderResponse
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
                    " to method get_slides_placeholder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_slides_placeholder`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_slides_placeholder`")  # noqa: E501
        # verify the required parameter 'placeholder_index' is set
        if not request.placeholder_index:
            raise ValueError("Missing the required parameter `request.placeholder_index` when calling `get_slides_placeholder`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['placeholderIndex'] = request.placeholder_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

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
            '/slides/{name}/slides/{slideIndex}/placeholders/{placeholderIndex}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PlaceholderResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_slides_placeholders(self, request, **kwargs):  # noqa: E501
        """Read slide placeholders info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_placeholders(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_placeholdersRequest request: get_slides_placeholders request object
        :return: PlaceholdersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_slides_placeholders_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_slides_placeholders_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_slides_placeholders_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide placeholders info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_slides_placeholders_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_slides_placeholdersRequest request: get_slides_placeholders request object
        :return: PlaceholdersResponse
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
                    " to method get_slides_placeholders" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_slides_placeholders`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_slides_placeholders`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

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
            '/slides/{name}/slides/{slideIndex}/placeholders', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PlaceholdersResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
