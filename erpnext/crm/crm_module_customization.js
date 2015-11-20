// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors


cur_frm.cscript.refresh = function(doc,cdt,cdn){
	cur_frm.toggle_enable('user_input', doc.__islocal);
	if(doc.naming_series=='CUST-')
		cur_frm.toggle_enable('customer_code', doc.__islocal);

	var last_route = frappe.route_history.slice(-2, -1)[0];
	if(last_route && last_route[0]==="Form") {
		var doctype = last_route[1],
		docname = last_route.slice(2).join("/");

	if(["Customer", "Quotation", "Sales Order", "Sales Invoice", "Delivery Note",
		"Installation Note", "Opportunity", "Warranty Claim", "Maintenance Visit",
		"Maintenance Schedule"]
		.indexOf(doctype)!==-1) {
		var refdoc = frappe.get_doc(doctype, docname);
		if((refdoc.doctype == "Quotation" && refdoc.quotation_to=="Customer") ||
			(refdoc.doctype == "Opportunity" && refdoc.enquiry_from=="Customer") ||
			!in_list(["Opportunity", "Quotation"], doctype)) {
				cur_frm.set_value("customer_code",refdoc.customer_code);
				
		}
	}

}
	
}

cur_frm.add_fetch('customer','customer_code','customer_code');

cur_frm.add_fetch('city','state','state');
cur_frm.add_fetch('city','district','district');
cur_frm.add_fetch('city','country','country');

