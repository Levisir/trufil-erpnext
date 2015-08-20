// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch('customer','customer_name','customer_name');
cur_frm.add_fetch('customer','customer_code','customer_code');

// Method to get address details
cur_frm.cscript.admin_address = function(doc,cdt,cdn){

	erpnext.utils.get_address_display(this.frm, "admin_address","admin_address_details");
}


//frappe call for retriveing administrative contact details and setting all details to a field
cur_frm.cscript.administrative_contact = function(doc,cdt,cdn){
	frappe.call({
			method:"erpnext.crm.doctype.order_register.order_register.get_contact_details",
			args:{"contact": doc.administrative_contact},
			callback: function(r) {
				if (r.message){
					doc.administrative_contact_details = (r.message['contact_display'] + '<br>' + r.message['contact_person'] + '<br>' + r.message['contact_email'] + '<br>' + r.message['contact_mobile'] + '<br>' + r.message['contact_personal_email'])
					refresh_field('administrative_contact_details')
				}
				
			}
		});

}


//frappe call for retriveing billing contact details and setting all details to a field
cur_frm.cscript.billing_contact = function(doc,cdt,cdn){
	frappe.call({
			method:"erpnext.crm.doctype.order_register.order_register.get_contact_details",
			args:{"contact": doc.billing_contact},
			callback: function(r) {
				if (r.message){
					doc.billing_contact_details = (r.message['contact_display'] + '<br>' + r.message['contact_person'] + '<br>' + r.message['contact_email'] + '<br>' + r.message['contact_mobile'] + '<br>' + r.message['contact_personal_email'])
					refresh_field('billing_contact_details')
				}
				
			}
		});

}


// Return query for getting administrative contact name in link field
cur_frm.fields_dict['administrative_contact'].get_query = function(doc) {
	return {
		filters: {
			
			"admin_contact": 1
		}
	}
}

// Return query for getting billing contact name in link field
cur_frm.fields_dict['billing_contact'].get_query = function(doc) {
	return {
		filters: {
			
			"billing_contact": 1
		}
	}
}


// Return query for getting admin address details
cur_frm.fields_dict['admin_address'].get_query = function(doc) {
	return {
		filters: {
			
			"address_type": 'Administrative'
		}
	}
}