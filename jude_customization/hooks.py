# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "jude_customization"
app_title = "Jude Customization"
app_publisher = "Anthony Emmanuel, github.com/mymi14ss"
app_description = "Custom utilities"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mymi14s@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jude_customization/css/jude_customization.css"
# app_include_js = "/assets/jude_customization/js/jude_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/jude_customization/css/jude_customization.css"
# web_include_js = "/assets/jude_customization/js/jude_customization.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "jude_customization.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "jude_customization.install.before_install"
# after_install = "jude_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jude_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}

    "HSE Meeting Notice Board":
        {
            "on_submit": "jude_customization.client.create_note_from_meeting_notice_board",
        },
    "Leave Application":{
        "on_update": "jude_customization.client.send_leave_application_email",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jude_customization.tasks.all"
# 	],
# 	"daily": [
# 		"jude_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"jude_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jude_customization.tasks.weekly"
# 	]
# 	"monthly": [
# 		"jude_customization.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "jude_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "jude_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jude_customization.task.get_dashboard_data"
# }
