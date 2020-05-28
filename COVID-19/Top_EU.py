import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('date_covid19')
data1 = data[((data.popData2018.notnull() == True) & (data.continentExp == 'Europe')) & (data.popData2018 > 150000)]
deaths = data1.groupby('countriesAndTerritories').sum().deaths.reset_index()
population = data1.groupby('countriesAndTerritories').mean().popData2018.reset_index()
death_population = deaths.merge(population)
order_deaths = death_population.sort_values(by=['deaths'], ascending=False)
top_10_deaths = order_deaths.head(10).reset_index()
percent = lambda row: row['deaths']/row['popData2018']*100
death_population['ratio'] = death_population.apply(percent, axis = 1)
order_death_population = death_population.sort_values(by=['ratio'], ascending=False)
top_10_ratio = order_death_population.head(10).reset_index(drop=True)
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}%'.format(round(height,3)) ,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


plt.figure(figsize=(8,12))
ax1 = plt.subplot(2, 1, 1)
bars1 = plt.bar(range(len(top_10_ratio.deaths)), top_10_ratio.ratio)
yticks = [round(i, 2) for i in top_10_ratio.ratio]
ax1.set_yticks([i/100.0 for i in range(10)])
ax1.set_xticks(range(10))
ax1.set_xticklabels(top_10_ratio.countriesAndTerritories, rotation= 30)
autolabel(bars1, ax1)
plt.title('Top 10 european countries with most deaths per population')
plt.ylabel('percentage of deaths per population')
ax2 = plt.subplot(2, 1, 2)
bars2 = plt.bar(range(10), top_10_deaths.deaths, color='black')
for rect in bars2:
    height = rect.get_height()
    ax2.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')
ax2.set_xticks(range(10))
ax2.set_xticklabels(top_10_deaths.countriesAndTerritories, rotation = 30)
ax2.set_yticks([i*5000 for i in range(10)])
ax2.set_yticks([i*5000 for i in range(10)])
plt.title('Top countries in Europe with most deaths from COVID-19')
plt.ylabel('total deaths')
plt.subplots_adjust(hspace=0.5)
plt.show()