from datetime import datetime
import calendar

today = datetime.now()
htmlcal = calendar.HTMLCalendar()
print(htmlcal.formatmonth(2026, 7))