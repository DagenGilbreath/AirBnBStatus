from pyairbnb import calendar
from datetime import datetime, date, timedelta
import mac_imessage
import json
import argparse

parser = argparse.ArgumentParser(
                    prog='BnbStatus',
                    description='Scrapes Air BnB to get information on booking and status of a specific property',
                    epilog='')

parser.add_argument('-i', '--room_id', type=str, required=True, help="Room ID for the Air BnB Listing")
parser.add_argument('-a', '--api_key', type=str, required=True, help="Air BnB API Key")
parser.add_argument('-n', '--number', required=False,           help="Send iMessage to a number with listing info")
parser.add_argument('-r', '--range', type=int, required=False,  help="Date range to fetch listings, default is 14 days ahead",)
args = parser.parse_args()

# get dates
date_format = "%Y-%m-%d"
current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year

# fetch data from pyairbnb
calendar_data = calendar.get(args.room_id, current_month, current_year, args.api_key, "")

# write data to file
with open('calendar.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(calendar_data, indent=2))  

# set date range
dayRange = 14
if args.range:
    dayRange = args.range

# filter
report = ""
for day in calendar_data:
    for fields in day.get("days"):
        fDate = datetime.strptime(fields.get("calendarDate"), date_format).date()

        isAvailable = fields.get("available")
        isBookable = fields.get("bookable")
        isAvailableForCheckIn = fields.get("availableForCheckin")
        isAvailableForCheckOut = fields.get("availableForCheckOut")

        info = "Booked: "
        if not isAvailable:
            info += "✅"
        else:
            info += "❌"

        if fDate < date.today():
            continue
        elif fDate == date.today():
            info += " < TODAY"
        elif fDate > date.today() + timedelta(days=dayRange):
            break

        words = [fields.get("calendarDate"), info]
        words = ':\t'.join(words)

        report += words + "\n"

print(report)

if args.number:
    print("sending iMessage") 
    mac_imessage.send(
        message=report,
        phone_number=args.number,
        medium='imessage'
    ) 

             