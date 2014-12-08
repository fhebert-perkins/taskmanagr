def sorter(then):
	from datetime import datetime
	now = datetime.utcnow()
	delta = then-now
	if delta.days < 0: # if if deadline has passed
		return "l1"
	elif delta.seconds/3600 <= 12: # if less than 12 hours to deadline
		return "l1"
	elif delta.days <= 1: # if less than 24 hours to deadline
		return "l2"
	elif delta.days <= 2: # if less than 48 hours to deadline
		return "l3"
	elif delta.days <= 7: # if less than a week  to deadline
		return "l4"
	elif delta.days <= 14: # if less than two weeks to deadline
		return "l5"
	elif delta.days <= 30: # if deadline within the month
		return "l6"
	elif delta.days <= 90: # if deadline within the quarter
		return "l7"
	else:
		return "l8"

def format_dueDate(duedate):
	from datetime import date
	from datetime import datetime
	year = int(duedate.split("-")[0])
	month= int(duedate.split("-")[1])
	day  = int(duedate.split("-")[2])
	return datetime.combine(date(year, month, day), datetime.min.time())
