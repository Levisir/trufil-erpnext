# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate
from frappe.model.mapper import get_mapped_doc


class OrderRegister(Document):
	def validate(self):
		if self.order_date and self.contract:
			contract_doc=frappe.get_doc("Contract",self.contract)
			if getdate(self.order_date) < getdate(contract_doc.contract_start_date):
				frappe.throw("Work Order Date < Contract Start Date")
			# work_order_doc.quantity_received=sample_count[0][0]
			# work_order_doc.save()

#Getting contact details after selecting contact name
@frappe.whitelist()
def get_contact_details(contact):
	contact = frappe.get_doc("Contact", contact)
	out = {
		"contact_person": contact.get("name") or " ",
		"contact_display": " ".join(filter(None,
			[contact.get("first_name"), contact.get("last_name")])) or " ",
		"contact_email": contact.get("email_id") or " ",
		"contact_mobile": contact.get("mobile_no")or " ",
		"contact_phone": contact.get("phone") or " ",
		"contact_designation": contact.get("designation") or " ",
		"contact_department": contact.get("department") or " ",
		"contact_personal_email" : contact.get("personal_email") or " "
	}
	return out

@frappe.whitelist()
def get_wo_info(sales_order):
	qty_query =	"""
					select 
						total_qty
					from
						`tabSales Order`
					where
						name = '%s' 
				"""%(sales_order)
	query = """
				select 
					ifnull(sum(total_samples), 0) 
				from 
					`tabOrder Register` 
				where 
					sales_order = '%s'
			"""%(sales_order)
	so_total_qty = frappe.db.sql(qty_query, as_list=1)
	existing_sample_qty = frappe.db.sql(query, as_list=1)
	return (flt(so_total_qty[0][0]) - existing_sample_qty[0][0])

@frappe.whitelist()
def check_total_samples(doc, method):
	qty_query =	"""
					select 
						total_qty
					from
						`tabSales Order`
					where
						name = '%s' 
				"""%(doc.sales_order)
	query = """
				select 
					ifnull(sum(total_samples), 0) 
				from 
					`tabOrder Register` 
				where 
					sales_order = '%s'
			"""%(doc.sales_order)
	so_total_qty = frappe.db.sql(qty_query, as_list=1)
	existing_sample_qty = frappe.db.sql(query, as_list=1)

	if(flt(so_total_qty[0][0])) < (existing_sample_qty[0][0] + doc.total_samples):
		frappe.throw("Total Samples exceed's than {0}'s Total Qty".format(doc.sales_order))

@frappe.whitelist()
def create_sample_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.customer = source.customer
		target.order_id = source.name
		

	doclist = get_mapped_doc("Order Register", source_name, {
			"Order Register": {
				"doctype": "Sample Entry Register",
				"validation": {
					"docstatus": ["=", 1]
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=False)
	return doclist