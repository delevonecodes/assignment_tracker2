from datetime import datetime
import calendar

def get_month_info():
    today = datetime.now()
    current_year = today.strftime("%Y")
    current_month = today.strftime("%m") if today.strftime("%m")[0] != "0" else today.strftime("%m")[1:]
    cal = calendar.Calendar(6)
    info = []
    month_iter = list(cal.itermonthdays(int(current_year), int(current_month)))
    i = 0
    while i < len(month_iter):
        week = []
        while len(week) < 7 and i < len(month_iter):
            week.append(month_iter[i])
            i += 1
        info.append(week)
    print(info)
    return info, today.strftime("%B") + " " + current_year