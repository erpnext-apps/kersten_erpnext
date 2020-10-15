from __future__ import unicode_literals

import frappe
from frappe.website.doctype.web_page.web_page import get_web_blocks_html


def set_page_blocks(context):
	doc = context.get('doc')
	if doc and doc.get('doctype') == 'Item':
		if doc.get('content_type') != 'Page Builder':
			return

		out = get_web_blocks_html(doc.page_building_blocks)
		context.page_builder_html = out.html
		context.page_builder_scripts = out.scripts