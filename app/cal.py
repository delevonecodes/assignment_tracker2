from datetime import datetime
import calendar

def get_month_info():
    today = datetime.now()
    current_year = today.strftime("%Y")
    current_month = today.strftime("%m") if today.strftime("%m")[0] != "0" else today.strftime("%m")[1:]
    cal = calendar.Calendar(6)
    info = [[],[],[],[],[],]
    week = 0
    for i in cal.itermonthdays(int(current_year), int(current_month)):
        if len(info[week]) < 7:
            info[week].append(i)
        else:
            week += 1
            info[week].append(i)
    return info, today.strftime("%B") + " " + current_year