import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
#
# Load the data files
dirname = os.path.dirname(__file__)

countries_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_countries.xlsx')
years_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_years.xlsx')
wipo_file = os.path.join(dirname, 'data', 'PatentSearch', 'WIPO', 'patents_wipo_raw.xls')

graph_path_wipo_years = os.path.join(dirname, r'graphs/wipo_years')
graph_path_wipo_countries = os.path.join(dirname, r'graphs/wipo_countries')
graph_path_countries_Espacenet = os.path.join(dirname, r'graphs/countries_Espacenet')
graph_path_years_Espacenet = os.path.join(dirname, r'graphs/years_Espacenet')

countries_data = pd.read_excel(countries_file)
publication_data = pd.read_excel(years_file)

wipo_data = pd.read_excel(wipo_file, header = 5)

populations_file = os.path.join(dirname, r'data/populations.xlsx')  # data from https://www.census.gov/data-tools/demo/idb/#/table?dashboard_page=country&COUNTRY_YR_ANIM=2025&menu=tableViz, January 2025
data_populations = pd.read_excel(populations_file, header=1)
data_populations["Name"] = data_populations["Name"].str.upper()

#data conversions
wipo_data['Application Date'] = pd.to_datetime(wipo_data['Application Date'], format='%d.%m.%Y')
wipo_data['Year'] = wipo_data['Application Date'].dt.year
# Map ISO-2 country codes to full names
country_mapping = dict(zip(data_populations['GENC'], data_populations['Name']))
wipo_data['Country Full Name'] = wipo_data['Country'].map(country_mapping)
countries_data['Countries (family)'] = countries_data['Countries (family)'].map(country_mapping)

wipo_data_withdate = wipo_data.dropna(subset=['Year'])
wipo_data_withdate['Year'] = wipo_data_withdate['Year'].astype(int)
# Plot 1: Number of patents per year
patents_per_year = wipo_data_withdate.groupby('Year').size()
plt.figure(figsize=(10, 6))
ax = patents_per_year.plot(kind='line')
years = patents_per_year.index
x_tick_list = [min(years)] + [x for x in years if x%5==0] + [max(years)]
x_tick_list = sorted(set(x_tick_list))

plt.xticks(x_tick_list, labels=x_tick_list, rotation=0)
plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1)) 
ax.tick_params(axis='x', which='major', color='black', width=1.5, length=10)
ax.tick_params(axis='x', which='minor', color='black', width=1.5, length=5)
ax.grid(which='major', axis='y', linestyle='-')
ax.set_axisbelow(True)


plt.title('Number of Patents Published Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Patents')
# plt.xticks(x_tick_list)
plt.minorticks_on()
plt.tight_layout()
# plt.show()
plt.savefig(graph_path_wipo_years)
plt.close()

# Plot 2: Number of patents per country
patents_per_country = wipo_data['Country Full Name'].value_counts()
plt.figure(figsize=(10, 6))
patents_per_country.plot(kind='barh')
plt.title('Number of Patents Published Per Country')
plt.xlabel('Number of Patents')
plt.ylabel('Country')
plt.tight_layout()
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
# plt.show()
plt.savefig(graph_path_wipo_countries)
plt.close()

# Plot data for "Countries (family)"
plt.figure(figsize=(10, 6))
countries_data = countries_data.dropna(subset=['Countries (family)'])
plt.barh(countries_data['Countries (family)'], countries_data['Number of documents'])
plt.xlabel('Country')
plt.ylabel('Count')
plt.title('Patent Families by Country')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.tight_layout()
plt.grid(axis='x', linestyle='-', alpha=0.7)
ax = plt.gca()
ax.set_axisbelow(True)
# plt.show()
plt.savefig(graph_path_countries_Espacenet)
plt.close()

# Plot data for "Earliest publication date (family)"
plt.figure(figsize=(10, 6))
plt.plot(publication_data['Earliest publication date (family)'], publication_data['Number of documents'])
plt.xlabel('Earliest Publication Date')
plt.ylabel('Count')
plt.title('Earliest Publication Date (Family)')
plt.grid(axis='y', linestyle='-', alpha=0.7)
plt.tight_layout()
# plt.show()
plt.savefig(graph_path_years_Espacenet)
plt.close()