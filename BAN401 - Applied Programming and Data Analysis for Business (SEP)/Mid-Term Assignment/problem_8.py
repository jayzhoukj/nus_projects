# Import required packages
from datetime import datetime, time

# Given function to check if a given time is between the start and end time
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

def coffee_queue():
    weekdays = ["monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday"]

    # Prompt user for the day and check if its a valid day of the week, if not request for another input.
    day_of_week = input("Please enter the day: ")
    while not(day_of_week.lower() in weekdays):
        print("Please enter a valid day!")
        day_of_week = input("Please enter the day: ")

    # Prompt user for current hour (24-h format) and check if its a valid hour, if not request for another input.
    hour_of_day = input("Please enter the hour, 24h format: ")
    while not(hour_of_day.isdigit() and (int(hour_of_day) in list(range(24)))):
        print("Please enter a valid number!")
        hour_of_day = input("Please enter the hour, 24h format: ")
    hour_of_day = int(hour_of_day)

    # Prompt user for current minute of the hour and check if it is valid (between 0 and 59), if not request for another input.
    minutes = input("Please enter the minutes: ")
    while not(minutes.isdigit() and (int(minutes) in list(range(60)))):
        print("Please enter a valid number!")
        minutes = input("Please enter the minutes: ")
    minutes = int(minutes)

    # Use a few if-else gates to check if the given time falls within the long/medium/no queue periods. Print the corresponding queue status accordingly.
    if day_of_week.lower() == "saturday" or day_of_week == "sunday":
        print("There is no queue at this time.")
    elif isNowInTimePeriod(time(10,0), time(10,15), time(hour_of_day,minutes)) or isNowInTimePeriod(time(12,0), time(12,15), time(hour_of_day,minutes)) or isNowInTimePeriod(time(14,0), time(14,15), time(hour_of_day, minutes)) or isNowInTimePeriod(time(7,50), time(8,15), time(hour_of_day, minutes)):
        print("There is long queue at this time.")
    elif isNowInTimePeriod(time(11,30), time(12,0), time(hour_of_day,minutes)) or isNowInTimePeriod(time(16,0), time(16,15), time(hour_of_day, minutes)):
        print("There is medium queue at this time.")
    else:
        print("There is no queue at this time.")

coffee_queue()
