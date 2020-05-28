import pandas as pd
from matplotlib import pyplot as plt
import datetime

raw_data = pd.read_csv('date_covid19')
country = input('Which county would you like to see?')
data_1 = raw_data[['dateRep','cases', 'deaths', 'countriesAndTerritories']]
romania_data = data_1[(data_1.countriesAndTerritories== country) ]
convert_to_datetime = lambda x: datetime.date(int(x.split('/')[2]), int(x.split('/')[1]), int(x.split('/')[0]))
romania_data['date'] = romania_data['dateRep'].apply(convert_to_datetime)
rd = romania_data[romania_data.date >= datetime.date(2020, 1, 1)]
convert_to_short_date = lambda x: x.strftime('%d') + ' ' + x.strftime('%b')
rd['dat'] = rd.date.apply(convert_to_short_date)
if rd.cases.max() > 20000:
    c = 1000
elif rd.cases.max() > 5000:
    c = 500
elif rd.cases.max() > 1000:
    c = 250
else:
    c = 50

plt.figure(figsize=(20,10))
x_values = range(len(rd.cases), 0, -1)
ax = plt.subplot()
plt.grid()
plt.bar(x_values, rd.cases, label = 'daily cases', color = 'red')
plt.xlabel('dates')
plt.ylabel('amount')
yticks = [i*c for i in range(int(rd.cases.max()/c))]
yticks.append(rd.cases.max())
ax.set_yticks(yticks)
xticks = [i*7 for i in range(1, int(len(rd.cases)/7)+1)]
xticks.append(len(rd.cases))
ax.set_xticks(xticks)
xticklabels = [list(rd.dat)[-i*7] for i in range(1, int(len(rd.cases)/7)+1)]
xticklabels.append(rd.dat.iloc[0])
ax.set_xticklabels(xticklabels)
plt.title('COVID-19 cases in {}'.format(country))
plt.show()
