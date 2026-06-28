import datetime
d = datetime.date(2016, 2, 3)-datetime.date(2016, 1, 1)
print(d.days)
if int(d.days)>5:
    print("yes")