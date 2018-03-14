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

def name_selection_groups(ids):
    return 'sel_groups_' + '_'.join(str(it) for it in ids)


class GroupsView(models.Model):
    _inherit = 'res.groups'

    @api.model
    def _update_user_groups_view(self):
        super(GroupsView, self)._update_user_groups_view()

        view = self.env.ref('base.user_groups_view', raise_if_not_found=False)
        for app, kind, gs in self.get_groups_by_application():
            if app.xml_id in ('base.module_category_administration'):
                field_name = name_selection_groups(gs.ids)
                break

        # Use String.replace() to add group_system
        if field_name:
            xml_content = view.arch.replace('name="' + field_name + '"', 'name="' + field_name + '" groups="base.group_system"')
            view.with_context(lang=None).write({'arch': xml_content, 'arch_fs': False})
