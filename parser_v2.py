import csv
from ics import Calendar
from datetime import datetime, timedelta
import logging
import sys
import argparse
import os
from prettytable import PrettyTable
import tempfile
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_calendar(file_path):
    try:
        with open(file_path, 'r') as file:
            c = Calendar(file.read())
        logging.info("Loaded calendar with {} events".format(len(c.events)))
        return c
    except FileNotFoundError:
        logging.error("Could not find file: {}".format(file_path))
        sys.exit(1)

def download_calendar(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("Could not download calendar from URL: {}".format(url))
        sys.exit(1)
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(response.content)
        logging.info("Downloaded calendar from URL: {} to file: {}".format(url, file.name))
        return file.name

def load_people(file_path):
    try:
        with open(file_path, 'r') as file:
            people = set(file.read().split(', '))
        logging.info("Loaded {} people: {}".format(len(people), ', '.join(people)))
        return people
    except FileNotFoundError:
        logging.error("Could not find file: {}".format(file_path))
        sys.exit(1)

def group_events_by_person(c, people, start_date=None, end_date=None):
    events_by_person = {person: [] for person in people}
    for event in c.events:
        if start_date and event.begin.date() < start_date:
            continue
        if end_date and event.end.date() > end_date:
            continue
        for person in people:
            if person in event.name:
                event_name = event.name.replace(person + ' - ', '').strip()
                start_date_event = event.begin.format('DD/MM/YYYY')
                end_date_event = event.end.format('DD/MM/YYYY')
                events_by_person[person].append((event_name, start_date_event, end_date_event))
    return events_by_person

def write_events_to_csv(events_by_person, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Start Date", "End Date", "Summary"])
        for person, events in events_by_person.items():
            for event in events:
                writer.writerow([person, event[0], event[1], event[2]])

def write_events_to_markdown(events_by_person, file_path):
    with open(file_path, 'w') as file:
        file.write("| Name | Event | Start | End |\n")
        file.write("| --- | --- | --- | --- |\n")
        for person, events in events_by_person.items():
            for event in events:
                file.write("| {} | {} | {} | {} |\n".format(person, event[0], event[1], event[2]))

def write_events_to_json(events_by_person, file_path):
    with open(file_path, 'w') as file:
        json.dump(events_by_person, file)

def write_events_to_html(events_by_person, file_path):
    with open(file_path, 'w') as file:
        file.write("<html>\n<head>\n<title>Calendar Events</title>\n</head>\n<body>\n")
        for person, events in events_by_person.items():
            file.write("<h2>{}</h2>\n".format(person))
            file.write("<ul>\n")
            for event in events:
                file.write("<li>{}</li>\n".format(event[0]))
            file.write("</ul>\n")
        file.write("</body>\n</html>")

def print_events_to_terminal(events_by_person):
    table = PrettyTable()
    table.field_names = ["Name", "Event", "Start", "End"]
    for person, events in events_by_person.items():
        for event in events:
            table.add_row([person, event[0], event[1], event[2]])
    print(table)

def main():
    parser = argparse.ArgumentParser(description='Process calendar events.')
    parser.add_argument("--format", choices=['csv', 'markdown'], default='csv', help='The output format of the events file.')
    parser.add_argument("--calendar", default='./calendar.ics', help='The path to the calendar file.')
    parser.add_argument("--start", type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='The start date of the date range.')
    parser.add_argument("--end", type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='The end date of the date range.')
    parser.add_argument("--next-sprint", action='store_true', help='Output events for the next 3 weeks.')
    parser.add_argument("--timezone", default='UTC', help='The timezone of the events.')
    parser.add_argument("--file", help='The path to the calendar file.')
    parser.add_argument("--url", help='The URL of the calendar file.')
    
    args = parser.parse_args()

    if args.file:
        calendar_file_path = args.file
    elif args.url:
        calendar_file_path = download_calendar(args.url)
    else:
        calendar_file_path = './calendar.ics'

    if os.path.exists('./people.csv'):
        people_file_path = './people.csv'
    else:
        logging.warning("People file not found, running for all people in the calendar.")
        people_file_path = None

    output_file_path = 'events-{}.{}'.format(datetime.now().strftime('%Y-%m-%d'), 'csv' if args.format == 'csv' else 'md')

    c = load_calendar(calendar_file_path)
    if people_file_path:
        people = load_people(people_file_path)
    else:
        people = set()
        for component in c.events:
            if component.name == "VEVENT":
                for person in component.get('summary').split(','):
                    people.add(person.strip())
        logging.info("Loaded people from calendar: {}".format(people))

    start_date = args.start
    end_date = args.end
    if args.next_sprint:
        start_date = datetime.now().date()
        end_date = start_date + timedelta(weeks=3)

    events_by_person = group_events_by_person(c, people, start_date, end_date)

    if args.format == 'csv':
        write_events_to_csv(events_by_person, output_file_path)
    elif args.format == 'markdown':
        write_events_to_markdown(events_by_person, output_file_path)
    elif args.format == 'json':
        write_events_to_json(events_by_person, output_file_path)
    elif args.format == 'html':
        write_events_to_html(events_by_person, output_file_path)
    else:
        write_events_to_csv(events_by_person, output_file_path)

    print_events_to_terminal(events_by_person)

if __name__ == "__main__":
    main()