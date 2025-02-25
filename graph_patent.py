import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
#
# Load the data files
dirname = os.path.dirname(__file__)

countries_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_countries.xlsx')
years_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_years.xlsx')
wipo_file = os.path.join(dirname, 'data', 'PatentSearch', 'WIPO', 'patents_wipo_polymer.xls')

graph_path_wipo_years = os.path.join(dirname, r'graphs/wipo_years')
graph_path_wipo_countries = os.path.join(dirname, r'graphs/wipo_countries')
graph_path_countries_Espacenet = os.path.join(dirname, r'graphs/countries_Espacenet')
graph_path_years_Espacenet = os.path.join(dirname, r'graphs/years_Espacenet')
graph_path_publication_and_patent = os.path.join(dirname, r'graphs/pulications_and_patents')

countries_data = pd.read_excel(countries_file)
publication_data = pd.read_excel(years_file)

wipo_data = pd.read_excel(wipo_file, header = 5)

populations_file = os.path.join(dirname, r'data/populations.xlsx')  # data from https://www.census.gov/data-tools/demo/idb/#/table?dashboard_page=country&COUNTRY_YR_ANIM=2025&menu=tableViz, January 2025
data_populations = pd.read_excel(populations_file, header=1)
data_populations["Name"] = data_populations["Name"].str.upper()

#data conversions
wipo_data['Application Date'] = pd.to_datetime(wipo_data['Application Date'], format='%d.%m.%Y')
wipo_data['Year'] = wipo_data['Application Date'].dt.year
patents_administered_by_wipo = len(wipo_data[wipo_data['Country'] == "WO"])

print(f"{patents_administered_by_wipo} patents administrated by WIPO")

# Map ISO-2 country codes to full names
country_mapping = dict(zip(data_populations['GENC'], data_populations['Name']))
country_mapping['KR'] = "SOUTH KOREA"
wipo_data['Country Full Name'] = wipo_data['Country'].map(country_mapping)
countries_data['Countries (family)'] = countries_data['Countries (family)'].map(country_mapping)

def color_bar_by_label(bars, labels, label_to_color, color="coral"):
    for bar, label in zip(bars, labels):
        if label == label_to_color:
            bar.set_color(color)

# Plot data for "Countries (family)"
plt.figure(figsize=(10, 6))
countries_data = countries_data.dropna(subset=['Countries (family)'])
countries_data = countries_data[countries_data['Number of documents'] > 1]
bars = plt.barh(countries_data['Countries (family)'], countries_data['Number of documents'])
plt.ylabel('Country')
plt.xlabel('Count')
plt.title('Patent Families by Country (Only > 1)')
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.tight_layout()
plt.grid(axis='x', linestyle='-', alpha=0.9, which="major")
plt.grid(axis='x', linestyle='--', alpha=0.7, which="minor")
ax = plt.gca()
ax.set_xscale('log')
ax.set_axisbelow(True)

for bar, count in zip(bars, countries_data['Number of documents']):
        y = bar.get_y() + bar.get_height() / 2  # Center the text vertically
        available_space_percent = count/max(countries_data['Number of documents']) 
        x = bar.get_x() + count*1.05
        ax.text(x, y, count, va='center', ha='left', color='Black', fontsize=8, weight='bold', backgroundcolor='none')

color_bar_by_label(bars, countries_data['Countries (family)'], "CHINA", color="coral")

# plt.show()
plt.savefig(graph_path_countries_Espacenet)
plt.close()

# Plot data for "Earliest publication date (family)"
plt.figure(figsize=(10, 6))
plt.plot(publication_data['Earliest publication date (family)'], publication_data['Number of documents'], marker = 'o', color="C0")
plt.xlabel('Earliest Publication Date')
plt.ylabel('Count')
plt.title('Earliest Publication Date (Family)')
plt.grid(axis='y', linestyle='-', alpha=0.7)
ax = plt.gca()

years = range(min(publication_data['Earliest publication date (family)']), max(publication_data['Earliest publication date (family)']) + 2)
x_tick_list = [min(years)] + [x for x in years if x%5==0] + [max(years)]
x_tick_list = sorted(set(x_tick_list))

plt.xticks(x_tick_list, labels=x_tick_list, rotation=0)
plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1)) 
ax.set_xlim(1980, 2025)
plt.tight_layout()
# plt.show()
plt.savefig(graph_path_years_Espacenet)

years_file = os.path.join(dirname, r'data/years_polymer_wos.xlsx')  
data_years = pd.read_excel(years_file)
data_years = data_years[data_years["Publication Years"]!= 2025]
plt.plot(data_years["Publication Years"], data_years["Count"], marker = 'o', color="C1")
handle_patents = Line2D([0], [0], color="C0", linestyle="-", label="Patents")
handle_pub = Line2D([0], [0], color="C1", linestyle="-", label="Publications")
plt.legend(handles = [handle_pub, handle_patents])
plt.xlabel('(Earliest) Publication Date')

plt.savefig(graph_path_publication_and_patent)
ax = plt.gca()
ax.set_xlim(2010, 2025)
plt.savefig(graph_path_publication_and_patent + "_lim")
plt.close()
