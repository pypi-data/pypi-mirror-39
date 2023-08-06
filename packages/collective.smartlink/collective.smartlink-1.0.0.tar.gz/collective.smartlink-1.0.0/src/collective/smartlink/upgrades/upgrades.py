# -*- coding: utf-8 -*-

from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from remove_internal_link import fix_internal_link_field

import logging

logger = logging.getLogger(__name__)


default_profile = 'profile-collective.smartlink:default'


def to_1100(context):
    """
    """
    logger.info('Upgrading collective.smartlink to version 1100')
    fti = queryUtility(IDexterityFTI, name="Link", default=None)
    if not fti:
        return

    logger.info('Changing model_file for Link type.')
    fti._updateProperty('model_file', 'plone.app.contenttypes.schema:link.xml')

    fix_internal_link_field(context)
