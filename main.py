import calendar


def linkify(year, month, day, style):
    return f'[{day}](#{year}{str(month).zfill(2)}{str(day).zfill(2)})'


def add_notes(month_calendar):
    while True:
        message = "Enter the day you want to add note (or 'exit' to finish): "
        date = input(message)
        if date.lower() == 'exit':
            break
        try:
            date = int(date)
            if 1 <= date <= 31:
                note = input("Enter note for this date: ")
                color = input("Enter color for this note: ")
                month_calendar[date].append((note, color))
                print(f"Note added for {date}.")
            else:
                message = "Invalid date. Please enter \
                           a valid day between 1 and 31."
                print(message)
        except ValueError:
            print("Invalid input. Please enter a valid day as a number.")
    return month_calendar


# Prompt user for year
year = input("Enter the year: ")
while not year.isdigit() or int(year) <= 0:
    year = input("Invalid input. Please enter a valid year: ")
year = int(year)

# Prompt user for month
message = "Enter the month (as a number): "
month = input(message)
while not month.isdigit() or not 1 <= int(month) <= 12:
    message = "Invalid input. Please enter a valid month (as a number): "
    month = input(message)
month = int(month)

# Create calendar and add notes
month_calendar = {day: [] for day in range(1, calendar.monthrange
                                           (year, month)[1] + 1)}
month_calendar = add_notes(month_calendar)

# Generate Markdown file
output = f'# {calendar.month_name[month]} {year}\n\n'

locale_weekdays = [{'en_US': 'Mon', 'it_IT': 'Lun'},
                   {'en_US': 'Tue', 'it_IT': 'Mar'},
                   {'en_US': 'Wed', 'it_IT': 'Mer'},
                   {'en_US': 'Thu', 'it_IT': 'Gio'},
                   {'en_US': 'Fri', 'it_IT': 'Ven'},
                   {'en_US': 'Sat', 'it_IT': 'Sab'},
                   {'en_US': 'Sun', 'it_IT': 'Dom'},]

weekdays = [locale_weekdays[i]['it_IT'] for i in range(7)]
calendar.setfirstweekday(calendar.MONDAY)

output += '| ' + ' | '.join(weekdays) + ' |\n'
output += '| ' + ' | '.join(['---'] * len(weekdays)) + ' |\n'

raw_calendar = calendar.monthcalendar(year, month)

# Find the maximum width of the notes
max_note_width = max(len(note) for day_notes in month_calendar.values() for note, _ in day_notes)

for week in raw_calendar:
    week_output = '| '
    for day in week:
        if day != 0:
            # Check if there are notes for this day
            if month_calendar[day]:
                notes_html = ' - ' + ', '.join([f'<span style="color: {color};\
                                                ">{note.ljust(max_note_width)}</span>' for note,
                                                color in month_calendar[day]])
            else:
                notes_html = ''
            week_output += f'[{day}](#{year}{str(month).zfill(2)}{str(day).zfill(2)}){notes_html} | '
        else:
            week_output += '  | '
    output += week_output[:-1] + '|\n'

# Write to file
file_name = f"{month:02d}_{year}.md"
with open(file_name, 'w') as f:
    f.write(output)

print(f"Markdown file saved as {file_name}")
