import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from matplotlib.ticker import MultipleLocator
# Load the data files
dirname = os.path.dirname(__file__)
affiliations_file = os.path.join(dirname, r'data/affiliations_wos.xlsx')  
years_file = os.path.join(dirname, r'data/years_wos.xlsx')  
countries_file = os.path.join(dirname, r'data/countries_wos.xlsx')  

polulations_file = os.path.join(dirname, r'data/populations.xlsx')  # data from www.census.gov, January 2025


affiliations_plot_path = os.path.join(dirname, r'graphs/affiliation')  # Replace with your local file path
affiliations_low_plot_path = os.path.join(dirname, r'graphs/affiliation_low')  # Replace with your local file path
affiliations_justnumbers_plot_path = os.path.join(dirname, r'graphs/affiliation_justnumbers')  # Replace with your local file path
years_plot_path = os.path.join(dirname, r'graphs/years')  # Replace with your local file path
years_cululative_plot_path = os.path.join(dirname, r'graphs/years_cumulative')
countries_plot_path = os.path.join(dirname, r'graphs/countries')  # Replace with your local file path
countries_population_plot_path = os.path.join(dirname, r'graphs/countries_population')  # Replace with your local file path
countries_count_per_population_plot_path = os.path.join(dirname, r'graphs/countries_count_per_population')  # Replace with your local file path
countries_justnumbers_plot_path = os.path.join(dirname, r'graphs/countries_justnumbers')  # Replace with your local file path


# Load the data into DataFrames
data_affiliations = pd.read_excel(affiliations_file)
data_years = pd.read_excel(years_file)
data_countries = pd.read_excel(countries_file)
data_populations = pd.read_excel(polulations_file, header=1)

data_populations["Name"] = data_populations["Name"].str.upper()

# manually change names, following line for manual debugging
# lookups = [country_name for country_name in data_countries['Countries/Regions'] if country_name not in list(data_populations["Name"])]
#england, wales, scotland, north ireland not available, just uk
#palestine not available
name_lookup_dict = {"PEOPLES R CHINA": "CHINA", 
                    "USA": "UNITED STATES", 
                    "SOUTH KOREA": "KOREA, SOUTH", 
                    "TURKIYE": "TURKEY", 
                    "CZECH REPUBLIC": "CZECHIA", 
                    "U ARAB EMIRATES": "UNITED ARAB EMIRATES",
                    "BOSNIA HERZEG": "BOSNIA and HERZEGOVINA"}


# Exclude small counts if needed (4 and below for this example)
data_affiliations_filtered = data_affiliations[data_affiliations['Count'] > 75]
data_affiliations_filtered_low = data_affiliations[data_affiliations['Count'] <25]
data_years_filtered = data_years  # No filtering applied here
data_countries_filtered = data_countries[data_countries['Count'] > 75]


populations = []
for country_name in data_countries['Countries/Regions']:
    if country_name in list(data_populations["Name"]):
        populations.append(int(str(list(data_populations[data_populations["Name"] == country_name]["Total Population"])[0]).replace('.','')))
    elif country_name in list(name_lookup_dict.keys()):
        populations.append(int(str(list(data_populations[data_populations["Name"] == name_lookup_dict[country_name]]["Total Population"])[0]).replace('.','')))
    else:
        populations.append(0)
        print(f"Warning: Population data for {country_name} not available, set to 0")

populations_filtered = []
for country_name in data_countries_filtered['Countries/Regions']:
    if country_name in list(data_populations["Name"]):
        populations_filtered.append(int(str(list(data_populations[data_populations["Name"] == country_name]["Total Population"])[0]).replace('.','')))
    elif country_name in list(name_lookup_dict.keys()):
        populations_filtered.append(int(str(list(data_populations[data_populations["Name"] == name_lookup_dict[country_name]]["Total Population"])[0]).replace('.','')))
    else:
        populations_filtered.append(0)
        # print(f"Warning: Population data for {country_name} not available, set to 0")

populations_filtered_scalefactor = [1/pop  if pop != 0 else 0 for pop in populations_filtered]

#-------------------------------
# Plot affiliations bar chart
#-------------------------------
plt.figure(figsize=(10, 6))
plt.barh(data_affiliations_filtered['Affiliations'], data_affiliations_filtered['Count'])
plt.title('Affiliations and Their Counts (Excluding Counts below 75)')
plt.ylabel('Affiliations')
plt.xlabel('Count')

ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(affiliations_plot_path)

#-------------------------------
# Plot affiliations bar chart low numbers
#-------------------------------
plt.figure(figsize=(10, 6))
plt.barh(data_affiliations_filtered_low['Affiliations'], data_affiliations_filtered_low['Count'])
plt.title('Affiliations and Their Counts (Excluding Counts above 25)')
plt.ylabel('Affiliations')
plt.xlabel('Count')

ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(affiliations_low_plot_path)




#-------------------------------
# Plot affiliations bar chart just numbers
#-------------------------------
plt.figure(figsize=(10, 6))
plt.plot(data_affiliations['Count'], data_affiliations['Affiliations'])
plt.title('Affiliations and Their Counts')
plt.ylabel('Affiliations, sorted by counts')
plt.xlabel('Count')

ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_yticklabels([])
ax.set_axisbelow(True)
ax.tick_params(axis='y', which='major', color='black', width=1.5, length=0)
ax.tick_params(axis='y', which='minor', color='black', width=1.5, length=0)
plt.axhline(y=len(data_affiliations_filtered), color='r', linestyle='-')
plt.axhline(y=len(data_affiliations) -len(data_affiliations_filtered_low), color='r', linestyle='-')
plt.tight_layout()
plt.savefig(affiliations_justnumbers_plot_path)

#-------------------------------
# Plot publication years bar chart
#-------------------------------

plt.figure(figsize=(10, 6))
plt.bar(data_years_filtered['Publication Years'], data_years_filtered['Count'])
x_tick_list = [min(data_years_filtered['Publication Years'])] + [x for x in data_years_filtered['Publication Years'] if x%5==0] + [max(data_years_filtered['Publication Years'])]
x_tick_list = sorted(list(set(x_tick_list)))
plt.title('Publication Years and Their Counts')
plt.xlabel('Publication Years')
plt.ylabel('Count')
plt.xticks(x_tick_list)
plt.minorticks_on()
plt.tight_layout()
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.tick_params(axis='x', which='major', color='black', width=1.5, length=10)
ax.tick_params(axis='x', which='minor', color='black', width=1.5, length=5)
ax.grid(which='major', axis='y', linestyle='-')
ax.set_axisbelow(True)
plt.savefig(years_plot_path)

#-------------------------------
# Plot publication years bar chart cumulative
#-------------------------------
data_years_filtered.sort_values("Publication Years", ascending=True, inplace=True)
data_years_filtered.reset_index(drop=True, inplace=True)
plt.figure(figsize=(10, 6))
cumulative_count = [data_years_filtered['Count'][0]]
for i in range(1,len(data_years_filtered['Count'])):
    cumulative_count.append(cumulative_count[i-1] + data_years_filtered['Count'][i])
plt.bar(data_years_filtered['Publication Years'], cumulative_count)
plt.title('Publication Years and Their Cumulative Counts')
plt.xlabel('Publication Years')
plt.ylabel('Cumulative Count')
plt.xticks(x_tick_list)
plt.minorticks_on()
plt.tight_layout()
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.tick_params(axis='x', which='major', color='black', width=1.5, length=10)
ax.tick_params(axis='x', which='minor', color='black', width=1.5, length=5)
ax.grid(which='major', axis='y', linestyle='-')
ax.set_axisbelow(True)
plt.savefig(years_cululative_plot_path)

#-------------------------------
# Plot countries/regions bar chart
#-------------------------------
plt.figure(figsize=(10, 6))
plt.barh(data_countries_filtered['Countries/Regions'], data_countries_filtered['Count'])
plt.title('Countries and Their Counts (Excluding Counts 75 and Below)')
plt.ylabel('Countries')
plt.xlabel('Count')
plt.tight_layout()
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
# ax2 = ax.twiny()
# ax2.plot(populations_filtered, data_countries_filtered['Countries/Regions'], color ="red")
# ax2.set_xlim(ax.get_xlim())
ax.set_axisbelow(True)
plt.savefig(countries_plot_path)

#-------------------------------
# Plot countries/regions population bar chart
#-------------------------------
scaled_counts = []
for i, scalefactor in enumerate(populations_filtered_scalefactor):
    scaled_counts.append(list(data_countries_filtered['Count'])[i] * scalefactor)

plt.figure(figsize=(10, 6))
plt.barh(data_countries_filtered['Countries/Regions'], populations_filtered)
plt.title('Countries and Their Populations (Excluding Counts 75 and Below)')
plt.ylabel('Countries')
plt.xlabel('Population')
plt.tight_layout()
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
plt.savefig(countries_population_plot_path)

#-------------------------------
# Plot countries/regions scaled by population bar chart
#-------------------------------

plt.figure(figsize=(10, 6))
plt.barh(data_countries_filtered['Countries/Regions'], scaled_counts)
plt.title('Countries Publication Count per Population (Excluding Counts 75 and Below)')
plt.ylabel('Countries/Regions')
plt.xlabel('Publication Count per Population')
plt.tight_layout()
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
plt.savefig(countries_count_per_population_plot_path)


#-------------------------------
# Plot countries/regions bar chart just numbers
#-------------------------------
plt.figure(figsize=(10, 6))
plt.plot(data_countries['Count'], data_countries['Countries/Regions'])
plt.title('Publication counts per country')
plt.ylabel('Countries')
plt.xlabel('Count')
plt.tight_layout()
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax2 = ax.twiny()
ax2.plot(populations, data_countries['Countries/Regions'], color ="red")
# ax2.set_xlim(ax.get_xlim())
ax.set_yticklabels([])
ax.set_axisbelow(True)
plt.savefig(countries_justnumbers_plot_path)