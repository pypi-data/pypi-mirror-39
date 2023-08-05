# -*- coding: utf-8 -*-
"""
License boilerplate should be used here.
"""

# python 3 imports
from __future__ import absolute_import, unicode_literals

# python imports
import logging

# 3rd. libraries imports
from appconf import AppConf

# django imports
from django.conf import settings  # noqa

logger = logging.getLogger(__name__)


class ExoMessagesConfig(AppConf):

    CH_CODE_PENDING_EMAIL = 'P'
    CH_CODE_VALIDATED_EMAIL = 'V'
    CH_CODE_PENDING_PASSWORD = 'W'

    CH_CODE = (
        (CH_CODE_PENDING_EMAIL, 'PENDING_VALIDATION_EMAIL'),
        (CH_CODE_VALIDATED_EMAIL, 'CONFIRMATION_VALIDATION_EMAIL'),
        (CH_CODE_PENDING_PASSWORD, 'PENDING_CHANGE_PASSWORD'),
    ) + getattr(settings, 'ADITIONAL_EXO_MESSAGES_CODE', ())

    CH_DEBUG = 10
    CH_INFO = 20
    CH_SUCCESS = 25
    CH_WARNING = 30
    CH_ERROR = 40

    CH_LEVEL = (
        (CH_DEBUG, 'debug'),
        (CH_INFO, 'info'),
        (CH_SUCCESS, 'success'),
        (CH_WARNING, 'warning'),
        (CH_ERROR, 'error'),
    )
