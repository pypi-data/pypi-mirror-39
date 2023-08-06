# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from rest_framework.exceptions import APIException


class JobCreationError(APIException):
    """ Error creating new Job. """
    status_code = 500
    default_detail = 'Error creating new Job.'
