# -*- coding: utf-8 -*-
from collective.smartlink import _
from plone.app.contenttypes.interfaces import ILink
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class ISmartLinkExtension(Interface):
    """ Marker interface for Links.
    """
