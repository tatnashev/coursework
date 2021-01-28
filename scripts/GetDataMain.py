import datetime as dt
from collections import defaultdict
from TextClass import Text
from GetDataFunc import get_data
from GetDataRevolution import get_data_revolution
import pandas as pd

# Getting dates
date = dt.date(day=6, month=11, year=1917)

# Open or create DataFrame
cols = ['Author', 'Date', 'Text']
if date == dt.date(day=14, month=11, year=1916):
    df = pd.DataFrame(columns=cols)
else:
    df = pd.read_csv('diary_entries.csv')

# Get Data
while date != dt.date(day=9, month=11, year=1917):
    flag_revolution = 0
    data = defaultdict(list)

    if date == dt.date(day=6, month=11, year=1917):
        flag_revolution = 1
        get_data_revolution(data)
    else:
        get_data(data, date)
    print('I collected data from {}'.format(date))

    # Record to the files and DataFrame
    for author, messages in data.items():
        with open(author + '.txt', 'a', encoding='UTF-8') as f:
            for message in messages:
                try:
                    f.write(message.date.strftime("%d.%m.%y"))
                    f.write('\n')
                    f.write(message.text)
                    f.write('\n\n')
                except UnicodeDecodeError:
                    print(message.text)

                df = pd.concat([df, pd.DataFrame([[author, message.date, message.text]], columns=cols)],
                               ignore_index=True)

    df.to_csv('diary_entries.csv', index=False)
    if flag_revolution:
        date += dt.timedelta(days=3)
    else:
        date += dt.timedelta(days=1)
