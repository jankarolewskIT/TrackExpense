import datetime
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# for row in cur.execute('SELECT total_budget FROM viewer_budget'):
#     print(row)

date = datetime.datetime.now()
day_of_date = int(date.strftime("%d"))
# print(day_of_date)

cur.execute(
    "update viewer_budget "
    "set total_budget=total_budget+"
    "(select income from viewer_profile, viewer_budget where viewer_budget.profile_id=viewer_profile.id and viewer_profile.pay_day=:day_of_date) "
    "WHERE viewer_budget.profile_id=(SELECT viewer_profile.id from viewer_profile,viewer_budget where viewer_profile.pay_day=:day_of_date and viewer_budget.profile_id = viewer_profile.id)",
    {"day_of_date": day_of_date})

for row in cur.execute('SELECT total_budget FROM viewer_budget'):
    print(row)
con.commit()
con.close()
