# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "kersten_erpnext"
app_title = "Kersten Erpnext"
app_publisher = "frappe"
app_description = "Custom App for building item web pages from page builder"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@frappe.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kersten_erpnext/css/kersten_erpnext.css"
# app_include_js = "/assets/kersten_erpnext/js/kersten_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/kersten_erpnext/css/kersten_erpnext.css"
# web_include_js = "/assets/kersten_erpnext/js/kersten_erpnext.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "kersten_erpnext/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

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

update_website_context = ["kersten_erpnext.templates.generators.item.item.set_page_blocks"]

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "kersten_erpnext.install.before_install"
# after_install = "kersten_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kersten_erpnext.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"kersten_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"kersten_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"kersten_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kersten_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kersten_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kersten_erpnext.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kersten_erpnext.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "kersten_erpnext.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = [
		{	"dt":"Custom Field",
			"filters": [["name", "in", [
				"Item-page_building_blocks",
				"Item-website_content_section",
				"Item-section_break_139",
				"Item-full_width",
				"Item-column_break_137",
				"Item-content_type"
				"Web Page Block-copy_from_doctype",
				"Web Page Block-copy_from_doctype"
		]]]
		},
		{"dt":"Custom Script", "filters": [["name", "in", [
				"Item-Client",
		]]]},
]

