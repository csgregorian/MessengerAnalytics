from datetime import datetime
from dateutil.parser import parse
import pickle
from sys import argv
from collections import namedtuple

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
            date = parse(line)
            name = next(lines)
        except Exception:
            if line != "":
                messages.append(Message(date, name, line))

    return messages

def init():
    if len(argv) >= 2:
        file_name = argv[1]
        parse(file_name)
    else:
        print("Filename must be supplied as an argument.")
        return 1

if __name__ == "__main__":
    init()




