import frappe
from datetime import datetime , timedelta
from frappe.utils import flt    

def set_hours_and_to_time(self,method):
    for row in self.time_logs:
        if not row.time and row.activity_type != "Break Time":
            frappe.throw(f"#Row{row.idx}: Field Time is mandetory")
            date_str = row.date
            time_str = row.time
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")

            # Parse the time string into a time object
            time_obj = datetime.strptime(str(time_str), "%H:%M").time()

            # Combine the date and time objects into a single datetime object
            combined_datetime = datetime.combine(date_obj.date(), time_obj)
            row.from_time = combined_datetime


@frappe.whitelist()       
def get_break_end_date(to_date , min):
    dt = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
    result = dt + timedelta(minutes=flt(min))
    time = str(dt.time())[0:-3]
    
    return result , time