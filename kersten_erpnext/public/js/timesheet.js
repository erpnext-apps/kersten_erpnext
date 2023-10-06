frappe.ui.form.on('Timesheet Detail', {
	time: function(frm, cdt, cdn) {
		let d = locals[cdt][cdn];
		let date = d.date
		let currentDate = `${date} ${d.time}`;
		d.from_date = currentDate
		frappe.model.set_value(cdt, cdn, 'from_time', currentDate)
		cur_frm.refresh_field('time_logs')
	},
	date: function(frm, cdt, cdn) {
		let d = locals[cdt][cdn];
		let date = d.date
		let currentDate = `${date} ${d.time}`;
		console.log(currentDate)
		d.from_date = currentDate
		frappe.model.set_value(cdt, cdn, 'from_time', currentDate)
		cur_frm.refresh_field('time_logs')
	},
	
})
frappe.ui.form.on('Timesheet', {
	refresh:function(frm){
		frm.add_custom_button(__('Add Break Time'), function () {
			
			var d = new frappe.ui.Dialog({
				title: __('Select Break Time'),
				fields: [{
					"label": "Break Time",
					"fieldname": "break_time",
					"fieldtype": "Select",
					"options": "Add 15 Mins Break\nAdd 30 Mins Break\nAdd 45 Mins Break\nAdd 60 Mins Break",
					"reqd": 1,
				}],
				primary_action: function () {
					var data = d.get_values();
					var to_time = frm.doc.time_logs[frm.doc.time_logs.length - 1]['to_time']
					var time = frm.doc.time_logs[frm.doc.time_logs.length - 1]['time']
					if(data.break_time == "Add 15 Mins Break"){
					var min = 15
					var hour = 0.25
						}
					if(data.break_time == "Add 30 Mins Break"){
						var min = 30
						var hour = 0.50
						}
					if(data.break_time == "Add 45 Mins Break"){
						var min = 45
						var hour = 0.75
						}
					if(data.break_time == "Add 60 Mins Break"){
						var min = 60
						var hour = 1
						}
					frappe.call({
						method: "kersten_erpnext.kersten_erpnext.timesheet.get_break_end_date",
						args: {
							to_date:to_time,
							min:min,
							time:time
						},
						callback: function (r) {
							if (!r.exc) {
								console.log(r)
								let row = frm.add_child("time_logs");
								row.from_time = to_time
								row.to_time = r.message[0];
								row.time = r.message[1];
								row.hours=hour;
								cur_frm.refresh_field('time_logs')
								d.hide();
							}
							
						}
					})
					
				},
				primary_action_label: __('Add')
			});
			d.show();
			 
		})
	}
})
