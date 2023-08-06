# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.browser.link_redirect_view import LinkRedirectView as Base  # noqa
from plone.app.contenttypes.browser.link_redirect_view import NON_RESOLVABLE_URL_SCHEMES  # noqa
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions import NotFound


class LinkRedirectView(Base):
    index = ViewPageTemplateFile('templates/link.pt')

    def absolute_target_url(self):
        """Compute the absolute target URL."""
        url = self.url()
        mtool = getToolByName(self.context, 'portal_membership')
        can_edit = mtool.checkPermission('Modify portal content', self.context)

        if self.context.remoteUrl.startswith('$'):
            # searching for the linked object
            obj = api.content.get(UID=url.split('/')[-1])

            if obj:
                return obj.absolute_url()
            else:
                # Broken Link
                if can_edit:
                    return None
                else:
                    raise NotFound()
        else:
            return super(LinkRedirectView, self).absolute_target_url()
