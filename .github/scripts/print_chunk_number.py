from datetime import datetime

today = datetime.today()
day = today.weekday()
ampm = 0 if today.strftime('%p') == 'AM' else 1
print(day * 2 + ampm)

