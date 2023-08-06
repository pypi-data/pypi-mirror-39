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

class MasterSlidesApi(ApiBase):

    def __init__(self, configuration = None, app_sid = None, app_key = None):
        super(MasterSlidesApi, self).__init__(configuration, app_sid, app_key)

    def get_master_slide(self, request, **kwargs):  # noqa: E501
        """Read presentation masterSlide info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_master_slide(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_master_slideRequest request: get_master_slide request object
        :return: MasterSlideResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_master_slide_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_master_slide_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_master_slide_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read presentation masterSlide info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_master_slide_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_master_slideRequest request: get_master_slide request object
        :return: MasterSlideResponse
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
                    " to method get_master_slide" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_master_slide`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_master_slide`")  # noqa: E501

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
            '/slides/{name}/masterSlides/{slideIndex}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='MasterSlideResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_master_slides_list(self, request, **kwargs):  # noqa: E501
        """Read presentation masterSlides info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_master_slides_list(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_master_slides_listRequest request: get_master_slides_list request object
        :return: MasterSlideListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_master_slides_list_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_master_slides_list_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_master_slides_list_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read presentation masterSlides info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_master_slides_list_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_master_slides_listRequest request: get_master_slides_list request object
        :return: MasterSlideListResponse
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
                    " to method get_master_slides_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_master_slides_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

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
            '/slides/{name}/masterSlides', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='MasterSlideListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_copy_master_slide_from_source_presentation(self, request, **kwargs):  # noqa: E501
        """Copy masterSlide from source presentation.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_copy_master_slide_from_source_presentation(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_copy_master_slide_from_source_presentationRequest request: post_copy_master_slide_from_source_presentation request object
        :return: MasterSlideResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_copy_master_slide_from_source_presentation_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_copy_master_slide_from_source_presentation_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_copy_master_slide_from_source_presentation_with_http_info(self, request, **kwargs):  # noqa: E501
        """Copy masterSlide from source presentation.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_copy_master_slide_from_source_presentation_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_copy_master_slide_from_source_presentationRequest request: post_copy_master_slide_from_source_presentation request object
        :return: MasterSlideResponse
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
                    " to method post_copy_master_slide_from_source_presentation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_copy_master_slide_from_source_presentation`")  # noqa: E501
        # verify the required parameter 'clone_from' is set
        if not request.clone_from:
            raise ValueError("Missing the required parameter `request.clone_from` when calling `post_copy_master_slide_from_source_presentation`")  # noqa: E501
        # verify the required parameter 'clone_from_position' is set
        if not request.clone_from_position:
            raise ValueError("Missing the required parameter `request.clone_from_position` when calling `post_copy_master_slide_from_source_presentation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501

        query_params = []
        if request.clone_from:
            query_params.append(('cloneFrom', request.clone_from))  # noqa: E501
        if request.clone_from_position:
            query_params.append(('cloneFromPosition', request.clone_from_position))  # noqa: E501
        if request.clone_from_password:
            query_params.append(('cloneFromPassword', request.clone_from_password))  # noqa: E501
        if request.clone_from_storage:
            query_params.append(('cloneFromStorage', request.clone_from_storage))  # noqa: E501
        if request.apply_to_all:
            query_params.append(('applyToAll', request.apply_to_all))  # noqa: E501
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
            '/slides/{name}/masterSlides', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='MasterSlideResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
