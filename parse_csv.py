import csv
import re
from datetime import datetime, date, timedelta

def main():
    file = "C:\\Users\\Pjmcnally\\Documents\programming\\google_calendar\\Midwest_Ultimate_Calendar_2018.csv"
    with open(file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]

    events = []
    for row in data:
        event_obj = event(*row)
        events.append(event_obj)
        print(event_obj)
        event_obj.print_dates()



class event():
    def __init__(self, date_str, name, divison, location, contact, email, website, audl):
        self.date_str = date_str
        self.date_list = self.parse_date_str(date_str)
        self.name = name
        self.division = divison
        self.location = location
        self.contact = contact
        self.email = email
        self.website = website
        self.AUDL = audl

    def __str__(self):
        basic_info = "\r\n{} {} at {} for {} players.".format(
            self.date_str,
            self.name,
            self.location,
            self.division,
        )

        if self.contact:
            contact_info = "\r\nContact {} at {}.".format(
                self.contact,
                self.email,
            )
        else:
            contact_info = ""

        if self.website:
            web_info = "\r\nSee {} for more info.".format(self.website)
        else:
            web_info = ""

        return "{}{}{}".format(
            basic_info,
            contact_info,
            web_info
        )

    def parse_date_str(self, date_str):
        """ Takes date string and returns list of dates.

            For example Jan 4-5 will return [Jan 4, Jan 5].
            Each item in the list will be a datetime object
        """
        dates = []
        year = "2018"  # Hard coded magic number. dang...
        date_format = "%b %d, %Y"

        if date_str == "TBD":
            return dates
        elif "-" in date_str:  # If a date range is indicated:
            p = "(?P<m1>\w{3})\s*(?P<d1>\d{1,2})-(?P<m2>\w{3})*(?P<d2>\s*\d{1,2})"
            match = re.search(p, date_str)
            beg_mon = match["m1"]
            beg_day = match["d1"]
            beg_date_str = "{} {}, {}".format(beg_mon, beg_day, year)
            beg_date = datetime.strptime(beg_date_str, date_format).date()

            end_mon = match["m2"] if match["m2"] else match["m1"]
            end_day = match["d2"]
            end_date_str = "{} {}, {}".format(end_mon, end_day, year)
            end_date = datetime.strptime(end_date_str, date_format).date()

            days = (end_date - beg_date).days
            for day in range(0, days + 1):
                cur_date = beg_date + timedelta(day)
                dates.append(cur_date)
        else:  # If only one date is indicated:
            date_str = "{}, {}".format(date_str, year)
            date = datetime.strptime(date_str, date_format).date()
            dates.append(date)

        return dates

    def print_dates(self):
        for date in self.date_list:
            print(date.strftime("%b %d, %Y"))


main()
