# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponseBase
from django.core.exceptions import PermissionDenied
from django.utils import six
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import viewsets
from rest_framework import views
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils import formatting
from ..permissions import TokenPermission
from ..utils import format_exception
from ..exceptions import AuthenticationFailed, APIException


show_detail = getattr(settings, "REST_EXCEPTION_DETAIL", False)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            # data = {'detail': exc.detail}
            data = format_exception(exc.status_code, exc.detail, exc.code, show_detail=show_detail)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            # data = {'detail': exc.detail}
            data = format_exception(exc.status_code, exc.detail, show_detail=show_detail)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        # data = {'detail': six.text_type(msg)}
        data = format_exception(status.HTTP_404_NOT_FOUND, six.text_type(msg), show_detail=show_detail)

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        # data = {'detail': six.text_type(msg)}
        data = format_exception(status.HTTP_403_FORBIDDEN, six.text_type(msg), show_detail=show_detail)

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
