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
                note = input("Enter note for this date (use '\\n' for new line): ")
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

# Define Italian weekday abbreviations
italian_weekday_abbr = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

# Define Italian month names
italian_month_names = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                       'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

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
month_calendar = {day: [] for day in range(1, calendar.monthrange(year, month)[1] + 1)}
month_calendar = add_notes(month_calendar)

# Generate Markdown file
output = f'# {italian_month_names[month]} {year}\n\n'

output += '| Giorno | Num | Nota/Appuntamento |\n'
output += '| ------ | --- | ----------------- |\n'

raw_calendar = calendar.monthcalendar(year, month)

for week in raw_calendar:
    for day in week:
        if day != 0:
            # Get the Italian weekday abbreviation
            weekday = italian_weekday_abbr[calendar.weekday(year, month, day)]
            # Check if there are notes for this day
            notes = '<br>'.join(['<span style="color: {};">{}</span>'.format(color, note.replace("\\n", "<br>")) for note, color in month_calendar[day]])
            output += f'| {weekday} | {day} | {notes} |\n'

# Write to file
file_name = f"{italian_month_names[month]}_{year}.md"
with open(file_name, 'w') as f:
    f.write(output)

print(f"Markdown file saved as {file_name}")
