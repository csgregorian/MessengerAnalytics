from datetime import datetime
from dateutil.parser import parse as dt_parse
import pickle
from sys import argv
from collections import namedtuple
from collections import OrderedDict

Message = namedtuple("Message", ["date", "name", "text"])

def parse(file_name):
    """
    Takes in an HTML file generated from the MessageSaver chrome extension
    and parses the results into a list of messages, with date/time and name
    metadata.
    """

    # Remove header data and standardize line break tags
    file = open(file_name).read()
    file = file.strip("<head><meta charset=\"UTF-8\"></head><body>")
    file = file.replace("<br />", "</br>")

    lines = iter(file.split("</br>"))

    messages = []
    
    # Default date if date isn't supplied in message
    date = datetime.now()
    name = ""

    while True:
        try:
            line = next(lines)
        except StopIteration:
            break
        
        try:
            date = dt_parse(line)
            assert dt_parse("2012") < date < datetime.now()
            name = next(lines)
        except Exception:
            if line != "":
                messages.append(Message(date, name, line))

    return messages

def analyze_weekdays(messages):
    weekdays = [0, 0, 0, 0, 0, 0, 0]
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"]
    
    for msg in messages:
        weekdays[msg.date.weekday()] += 1

    print("---Weekday frequency---")
    graph(weekdays, day_names)

def analyze_hours(messages):
    hours = [0 for i in range(24)]
    for msg in messages:
        hours[msg.date.hour] += 1

    print("---Hour frequency---")
    graph(hours, range(1, 25))

def analyze_months(messages):
    months = {(y, m): 0 for y in range(2012, datetime.now().year+1)
            for m in range(1, 13)}
    
    for msg in messages:
        try:
            months[(msg.date.year, msg.date.month)] += 1
        except KeyError:
            print(msg)

    print("---Month frequency---")
    months = OrderedDict(sorted(months.items()))
    graph(list(months.values()), list(months.keys()))



def run_analytics(messages):
    analyze_weekdays(messages)
    analyze_hours(messages)
    analyze_months(messages)

def graph(values, label, size=20):
    for i in range(len(values)):
        print(label[i], "->", "█" * round(values[i] / max(values) * size),
                values[i])



def init():
    if len(argv) >= 2:
        file_name = argv[1]
        messages = parse(file_name)
        print("Parsing done!")
    else:
        print("Filename must be supplied as an argument.")
        return 1

    run_analytics(messages)



if __name__ == "__main__":
    init()




