# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2015-2020 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Theme blueprint in order for template and static files to be loaded."""

from __future__ import absolute_import, print_function

from datetime import datetime, timedelta

import bleach
from flask import Blueprint
from flask_principal import ActionNeed
from invenio_access import Permission

from zenodo.modules.records.serializers.fields.html import ALLOWED_ATTRS, \
    ALLOWED_TAGS

blueprint = Blueprint(
    'zenodo_theme',
    __name__,
    template_folder='templates',
    static_folder='static',
)
"""Theme blueprint used to define template and static folders."""


@blueprint.app_template_filter('sanitize_html')
def sanitize_html(value):
    """Sanitizes HTML using the bleach library."""
    return bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    ).strip()


@blueprint.app_template_global()
def current_user_is_admin():
    """Returns ``True`` if current user has the ``admin-access`` permission."""
    return Permission(ActionNeed('admin-access')).can()


@blueprint.app_template_test('older_than')
def older_than(dt, **timedelta_kwargs):
    """Check if a date is older than a provided timedelta.

    :param dt: The datetime to check.
    :param timedelta_kwargs: Passed to ``datetime.timedelta(...)``.
    """

    return (datetime.utcnow() - dt) > timedelta(**timedelta_kwargs)
