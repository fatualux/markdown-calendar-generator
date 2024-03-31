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

def generate_css(font_name):
    css_content = f'''
  @font-face {{
        font-family: '{font_name}';
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }}
    body {{

        background-color: #f2f2f2;
        font-family: '{font_name}', Arial, sans-serif;
    }}
        table {{
            width: 33%;
            border-collapse: collapse;
            border-left: none;
            border-right: none;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #000000;
            text-align: center;
            border-left: none;
            border-right: none;
            border-collapse: collapse;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
    '''
    with open("calendar_style.css", "w") as css_file:
        css_file.write(css_content)
    print("CSS file generated: calendar_style.css")

# Define Italian weekday abbreviations
italian_weekday_abbr = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

# Define Italian month names
italian_month_names = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                       'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

# Prompt user for font name
font_name = input("Enter the font name: ")

# Create calendar and add notes
year = int(input("Enter the year: "))
month = int(input("Enter the month (as a number): "))

month_calendar = {day: [] for day in range(1, calendar.monthrange(year, month)[1] + 1)}
month_calendar = add_notes(month_calendar)

# Generate HTML file
output = f'<!DOCTYPE html>\n<html>\n<head>\n<title>{italian_month_names[month]} {year}</title>\n'
output += f'<link rel="stylesheet" type="text/css" href="calendar_style.css">\n</head>\n<body>\n'

# Generate table: in the first line put <h1>{italian_month_names[month]} {year}</h1>
output += f'<table border="1">\n<tr><th colspan="7"><h1>{italian_month_names[month]} {year}</h1></th></tr>\n'

raw_calendar = calendar.monthcalendar(year, month)

for week in raw_calendar:
    output += '<tr>'
    for day in week:
        if day != 0:
            # Get the Italian weekday abbreviation
            weekday = italian_weekday_abbr[calendar.weekday(year, month, day)]
            # Check if there are notes for this day
            notes = '<br>'.join(['<span style="color: {}; font-weight: bold;">{}</span>'.format(color, note.replace("\\n", "<br>")) for note, color in month_calendar[day]])
            output += f'<td>{weekday}</td><td>{day}</td><td>{notes}</td>'
        else:
            output += '<td></td><td></td><td></td>'
    output += '</tr>\n'

output += '</table>\n</body>\n</html>'

# Write HTML to file
html_file_name = f"{italian_month_names[month]}_{year}.html"
with open(html_file_name, 'w') as f:
    f.write(output)

print(f"HTML file saved as {html_file_name}")

# Generate CSS file
generate_css(font_name)
