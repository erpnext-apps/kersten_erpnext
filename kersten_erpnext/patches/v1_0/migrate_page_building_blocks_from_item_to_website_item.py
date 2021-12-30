import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	frappe.reload_doc('e_commerce', 'doctype' ,'website_item')
	frappe.reload_doc('stock', 'doctype' ,'item')

	custom_fields = {
		'Website Item': [
			dict(fieldname='website_content_section', label='Website Content Section',
				fieldtype='Section Break', insert_after='advanced_display_section'),
			dict(fieldname='content_type', label='Content Type', fieldtype='Select',
				insert_after='website_content_section', options='HTML\nPage Builder'),
			dict(fieldname='full_width', label='Full Width', fieldtype='Check',
				insert_after='content_type'),
			dict(fieldname='page_building_blocks', label='Page Building Blocks', fieldtype='Table',
				options='Web Page Block', insert_after='full_width'),
			dict(fieldname='jodit_editor', label='Website Description', fieldtype='HTML',
				insert_after='page_building_blocks'),
		]
	}

	create_custom_fields(custom_fields)
	frappe.db.sql("""update `tabItem` set published_in_website = 1
		where has_variants=1""")

	items = frappe.get_all('Website Item',
		fields=['name', 'item_code'], filters={'has_variants': 0})

	for item in items:
		blocks = frappe.get_all('Web Page Block', fields = ['add_bottom_padding', 'add_container',
			'add_shade', 'add_top_padding', 'hide_block', 'idx', 'web_template', 'web_template_values', 'owner', 'css_class'],
			filters = {'parent': item.item_code, 'parenttype': 'Item'})

		doc = frappe.get_doc('Website Item', item.name)
		doc.content_type = frappe.db.get_value('Item', item.item_code, 'content_type')
		doc.full_width = frappe.db.get_value('Item', item.item_code, 'full_width')
		for block in blocks:
			doc.append('page_building_blocks', block)
		doc.flags.ignore_validate = True
		doc.save()