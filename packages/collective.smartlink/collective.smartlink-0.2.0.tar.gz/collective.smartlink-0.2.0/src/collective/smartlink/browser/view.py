# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.link_redirect_view import LinkRedirectView as Base  # noqa
from plone.app.contenttypes.browser.link_redirect_view import NON_RESOLVABLE_URL_SCHEMES  # noqa
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class LinkRedirectView(Base):
    index = ViewPageTemplateFile('templates/link.pt')

    def absolute_target_url(self):
        """Compute the absolute target URL."""
        url = self.url()

        if self.context.remoteUrl.startswith('$'):
            # searching for the linked object
            obj = api.content.get(UID=url.split('/')[-1])
            return obj.absolute_url()
        else:
            return super(LinkRedirectView, self).absolute_target_url()
