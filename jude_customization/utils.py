from __future__ import unicode_literals
import os, pathlib
import json
import base64
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import LDAPSettings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html
from frappe.integrations.oauth2_logins import decoder_compat


# get site name
def get_system_site_name():
    # from frappe.utils import get_site_name
    # print(pathlib.Path().absolute())
    return "{0}/{1}".format(os.getcwd(), frappe.utils.cstr(frappe.local.site)) or None

# login permission
def is_logged_in():
    if frappe.session.user=='Guest':
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

# get auth user
@frappe.whitelist()
def get_auth_user():
    return frappe.get_doc("User", frappe.session.user) or None

# redirect user to user_type homepage
