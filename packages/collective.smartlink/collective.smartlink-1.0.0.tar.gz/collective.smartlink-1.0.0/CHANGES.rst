Changelog
=========


1.0.0 (2018-12-14)
------------------

- Version bump that needed to be done in the previous release :)
  [arsenico13]
- Fixed the upgrade step from 1000 to 1100: the upgrade now works even if the
  Link objects points to a deleted resource.
  When you run the upgrade, check the logs for more info.
  [arsenico13]
- Changes to link.pt to show a message if the internal link is broken and user
  can edit
  [arsenico13]
- Raise 404 if an internal link is broken and user can't edit
  [arsenico13]
- Reviewed some italian translations
  [arsenico13]


0.2.0 (2018-12-13)
------------------

Upgrade step required.

- Removed override for Link add/edit forms
  [arsenico13]
- Removed changes to the link schema (the 'schema' folder is still in the
  product just for avoid errors while upgrading: will be removed at the next
  version of the add-on)
  [arsenico13]
- Removed indexers
  [arsenico13]
- NEW: Added an output filter that changes every `resolveuid` for an internal
  link found in a page with the absolute_url of that plone object.
  [arsenico13]
- NEW: No more 'internal_link' field. Right now, all is done with the field
  `remoteUrl` as the standard Plone Link type.
  [arsenico13]
- link.pt: when the link is internal, the template shows the absolute url to
  the linked object. It's more human readable than the `resolveuid` link...
  [arsenico13]


0.1.1 (2018-09-28)
------------------

- Fixed view when link is broken [daniele]


0.1.0 (2017-09-13)
------------------

- Removed plone directives form deprecated [fdelia]
