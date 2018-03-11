# -*- coding: utf-8 -*-

import pytz
import datetime
import itertools
import logging

from collections import defaultdict
from itertools import chain, repeat
from lxml import etree
from lxml.builder import E

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.service.db import check_super
from odoo.tools import partition, pycompat

_logger = logging.getLogger(__name__)


#
# Functions for manipulating boolean and selection pseudo-fields
#
def name_boolean_group(id):
    return 'in_group_' + str(id)


def name_selection_groups(ids):
    return 'sel_groups_' + '_'.join(str(it) for it in ids)


def is_boolean_group(name):
    return name.startswith('in_group_')


def is_selection_groups(name):
    return name.startswith('sel_groups_')


def is_reified_group(name):
    return is_boolean_group(name) or is_selection_groups(name)


def get_boolean_group(name):
    return int(name[9:])


def get_selection_groups(name):
    return [int(v) for v in name[11:].split('_')]


def name_selection_groups(ids):
    return 'sel_groups_' + '_'.join(str(it) for it in ids)


class GroupsView(models.Model):
    _inherit = 'res.groups'

    @api.model
    def _update_user_groups_view(self):
        """ Modify the view with xmlid ``base.user_groups_view``, which inherits
            the user form view, and introduces the reified group fields.
        """
        if self._context.get('install_mode'):
            # use installation/admin language for translatable names in the view
            user_context = self.env['res.users'].context_get()
            self = self.with_context(**user_context)

        # We have to try-catch this, because at first init the view does not
        # exist but we are already creating some basic groups.
        view = self.env.ref('base.user_groups_view', raise_if_not_found=False)
        if view and view.exists() and view._name == 'ir.ui.view':
            group_no_one = view.env.ref('base.group_no_one')
            xml1, xml2 = [], []
            xml1.append(E.separator(string=_('Application Accesses'), colspan="2"))
            for app, kind, gs in self.get_groups_by_application():
                # hide groups in categories 'Hidden' and 'Extra' (except for group_no_one)
                attrs = {}
                if app.xml_id in ('base.module_category_hidden', 'base.module_category_extra', 'base.module_category_usability'):
                    attrs['groups'] = 'base.group_no_one'

                if app.xml_id in ('base.module_category_administration'):
                    attrs['groups'] = 'base.group_system'

                if kind == 'selection':
                    # application name with a selection field
                    field_name = name_selection_groups(gs.ids)
                    xml1.append(E.field(name=field_name, **attrs))
                    xml1.append(E.newline())
                else:
                    # application separator with boolean fields
                    app_name = app.name or _('Other')
                    xml2.append(E.separator(string=app_name, colspan="4", **attrs))
                    for g in gs:
                        field_name = name_boolean_group(g.id)
                        if g == group_no_one:
                            # make the group_no_one invisible in the form view
                            xml2.append(E.field(name=field_name, invisible="1", **attrs))
                        else:
                            xml2.append(E.field(name=field_name, **attrs))

                xml2.append({'class': "o_label_nowrap"})
                xml = E.field(E.group(*(xml1), col="2"), E.group(*(xml2), col="4"), name="groups_id", position="replace")
                xml.addprevious(etree.Comment("GENERATED AUTOMATICALLY BY GROUPS"))
                print("XML: " + str(xml))
                xml_content = etree.tostring(xml, pretty_print=True, encoding="unicode")
                print("xml_content: " + str(xml_content))
                view.with_context(lang=None).write({'arch': xml_content, 'arch_fs': False})
