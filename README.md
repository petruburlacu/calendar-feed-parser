# Calendar Event Processor
This script processes calendar events from an iCalendar file and outputs them in various formats. The script takes the following arguments:

--format: The output format of the events file. Valid options are csv, markdown, and table. Default is csv.
--file: The path to the calendar file.
--url: The URL of the calendar file.
--start: The start date of the date range. Must be in the format YYYY-MM-DD.
--end: The end date of the date range. Must be in the format YYYY-MM-DD.
--next-sprint: Output events for the next 3 weeks.
The script has the following dependencies:

argparse: For parsing command line arguments.
csv: For reading and writing CSV files.
datetime: For working with dates and times.
icalendar: For reading iCalendar files.
logging: For logging errors and messages.
os: For working with file paths and URLs.
sys: For exiting the script on errors.
tabulate: For formatting tables.
The script consists of the following functions:

load_calendar(calendar_file_path): Loads an iCalendar file from the specified file path and returns a Calendar object.
load_people(people_file_path): Loads a list of people from the specified file path and returns a list of strings.
get_date_range(start_date, end_date, next_sprint): Returns a tuple of start and end dates based on the specified arguments.
get_calendar_file_path(file_path, url): Returns the file path of the calendar file based on the specified arguments.
get_people_file_path(): Returns the file path of the people file.
get_output_file_path(output_format): Returns the file path of the output file based on the specified output format.
get_event_summaries(calendar): Returns a list of event summaries from the specified Calendar object.
group_events_by_person(calendar, people, start_date=None, end_date=None): Groups events in the specified Calendar object by person and returns a dictionary of events.
get_events(calendar, people, start_date=None, end_date=None): Returns a list of events from the specified Calendar object based on the specified arguments.
write_events_to_csv(events, output_file_path): Writes the specified list of events to a CSV file at the specified file path.
write_events_to_markdown(events, output_file_path): Writes the specified list of events to a Markdown file at the specified file path.
write_events_to_table(events, output_file_path): Writes the specified list of events to an ASCII formatted table file at the specified file path.
write_events_to_file(events, output_file_path, output_format): Writes the specified list of events to a file in the specified output format at the specified file path.
print_events(events): Prints the specified list of events to the console in an ASCII formatted table.
print_events_to_terminal(events): Prints the specified dictionary of events to the console in an ASCII formatted table.
The script also has a main() function that parses command line arguments, loads the calendar and people files, processes the events, writes the events to a file, and prints the events to the console.

To use the script, run the following command:

Replace <calendar_file_path> with the path to the iCalendar file, and <output_format> with the desired output format (csv, markdown, or table). You can also specify other optional arguments, such as --start and --end to filter events by date range.

The script will output the events to the console in an ASCII formatted table, and also write the events to a file in the specified output format.