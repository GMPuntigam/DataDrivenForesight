import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from matplotlib.ticker import MultipleLocator
# Load the data files
dirname = os.path.dirname(__file__)


populations_file = os.path.join(dirname, r'data/populations.xlsx')  # data from https://www.census.gov/data-tools/demo/idb/#/table?dashboard_page=country&COUNTRY_YR_ANIM=2025&menu=tableViz, January 2025
data_populations = pd.read_excel(populations_file, header=1)
data_populations["Name"] = data_populations["Name"].str.upper()


materialstrings = ["cement", "polymer", "ceramic", "metal"]

cutoffs_dict_upper = {"cement": 20, 
                      "polymer": 75,
                      "ceramic": 8,
                      "metal": 30}

cutoffs_dict_lower = {"cement": 6, 
                      "polymer": 15,
                      "ceramic": 2,
                      "metal": 8}

for materialstring in materialstrings:
    affiliations_file = os.path.join(dirname, r'data/affiliations_' + materialstring +'_wos.xlsx')  
    countries_file = os.path.join(dirname, r'data/countries_' + materialstring +'_wos.xlsx')  
    countries_population_plot_path = os.path.join(dirname, r'graphs/countries_population_' + materialstring)  # Replace with your local file path
    affiliations_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'')  # Replace with your local file path
    affiliations_low_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'_low')  # Replace with your local file path
    affiliations_justnumbers_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'_justnumbers')  # Replace with your local file path
    countries_plot_path = os.path.join(dirname, r'graphs/countries_' + materialstring +'')  # Replace with your local file path
    countries_count_per_population_plot_path = os.path.join(dirname, r'graphs/countries_count_' + materialstring +'_per_population')  # Replace with your local file path
    countries_justnumbers_plot_path = os.path.join(dirname, r'graphs/countries_' + materialstring +'_justnumbers')  # Replace with your local file path


    # Load the data into DataFrames
    data_affiliations = pd.read_excel(affiliations_file)
    data_countries = pd.read_excel(countries_file)
    uk_country_list = ["SCOTLAND", "NORTH IRELAND", "ENGLAND", "WALES"]
    for country in uk_country_list:
        if country not in data_countries["Countries/Regions"]:
            data_countries.loc[len(data_countries)] = [country, 0]

    # merge uk country values
    count = sum([list(data_countries[data_countries["Countries/Regions"] == country]["Count"])[0] for country in ["SCOTLAND", "NORTH IRELAND", "ENGLAND", "WALES"]])
    data_countries.loc[len(data_countries)] = ["UNITED KINGDOM", count]
    data_countries = data_countries[~data_countries["Countries/Regions"].isin(uk_country_list)]

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
                        "BOSNIA HERZEG": "BOSNIA AND HERZEGOVINA",
                        "BOSNIA HERCEG": "BOSNIA AND HERZEGOVINA"}


    # Exclude small counts if needed (4 and below for this example)
    data_affiliations_filtered = data_affiliations[data_affiliations['Count'] > cutoffs_dict_upper[materialstring]]
    data_affiliations_filtered_low = data_affiliations[data_affiliations['Count'] <cutoffs_dict_lower[materialstring]]
    data_countries_filtered = data_countries[data_countries['Count'] > cutoffs_dict_upper[materialstring]]


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
    plt.title(f'Affiliations and Their Counts (Excluding Counts below {cutoffs_dict_upper[materialstring]})')
    plt.ylabel('Affiliations')
    plt.xlabel('Count')
    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(affiliations_plot_path)
    plt.close()

    #-------------------------------
    # Plot affiliations bar chart low numbers
    #-------------------------------
    plt.figure(figsize=(10, 6))
    plt.barh(data_affiliations_filtered_low['Affiliations'], data_affiliations_filtered_low['Count'])
    plt.title(f'Affiliations and Their Counts (Excluding Counts above {cutoffs_dict_lower[materialstring]})')
    plt.ylabel('Affiliations')
    plt.xlabel('Count')

    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(affiliations_low_plot_path)
    plt.close()

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
    plt.close()
    #-------------------------------
    # Plot countries/regions bar chart
    #-------------------------------
    plt.figure(figsize=(10, 6))
    plt.barh(data_countries_filtered['Countries/Regions'], data_countries_filtered['Count'])
    plt.title(f'Countries and Their Counts (Excluding Counts {cutoffs_dict_upper[materialstring]} and Below)')
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
    plt.close()
    #-------------------------------
    # Plot countries/regions population bar chart
    #-------------------------------
    scaled_counts = []
    for i, scalefactor in enumerate(populations_filtered_scalefactor):
        scaled_counts.append(list(data_countries_filtered['Count'])[i] * scalefactor)

    plt.figure(figsize=(10, 6))
    plt.barh(data_countries_filtered['Countries/Regions'], populations_filtered)
    plt.title(f'Countries and Their Populations (Excluding Counts {cutoffs_dict_upper[materialstring]} and Below)')
    plt.ylabel('Countries')
    plt.xlabel('Population')
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.savefig(countries_population_plot_path)
    plt.close()

    #-------------------------------
    # Plot countries/regions scaled by population bar chart
    #-------------------------------

    plt.figure(figsize=(10, 6))
    plt.barh(data_countries_filtered['Countries/Regions'], scaled_counts)
    plt.title(f'Countries Publication Count per Population (Excluding Counts {cutoffs_dict_upper[materialstring]} and Below)')
    plt.ylabel('Countries/Regions')
    plt.xlabel('Publication Count per Population')
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.savefig(countries_count_per_population_plot_path)
    plt.close()

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
    plt.close()

df_years_all = pd.DataFrame()

for materialstring in materialstrings:
    
    years_file = os.path.join(dirname, r'data/years_' + materialstring +'_wos.xlsx')  
    data_years = pd.read_excel(years_file)
    # Ensure "Publication Years" is the index for merging
    data_years = data_years.set_index("Publication Years")

    # Rename the "Counts" column to the current materialstring
    data_years = data_years.rename(columns={"Counts": materialstring})

    # Merge with the result DataFrame, filling missing values with 0
    df_years_all = df_years_all.join(data_years, how="outer", rsuffix=f"_{materialstring}").fillna(0) if not df_years_all.empty else data_years

# Reset index to include "Publication Years" as a column
df_years_all = df_years_all.reset_index()


#Remove 2025, unreliable data
df_years_all = df_years_all[df_years_all["Publication Years"]!= 2025]

#reset column names 
df_years_all.columns = ["Publication Years"] + materialstrings

years_plot_path = os.path.join(dirname, r'graphs/years') 
years_cululative_plot_path = os.path.join(dirname, r'graphs/years_cumulative')
#-------------------------------
# Plot publication years bar chart
#-------------------------------

# plt.figure(figsize=(10, 6))
df_years_all.plot(x="Publication Years", y=materialstrings,
        kind="line", figsize=(10, 6))
# for materialstring in materialstrings:
#     plt.plot(df_years_all['Publication Years'], df_years_all[materialstring])
x_tick_list = [min(df_years_all['Publication Years'])] + [x for x in df_years_all['Publication Years'] if x%5==0] + [max(df_years_all['Publication Years'])]
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
plt.close()

#-------------------------------
# Plot publication years bar chart cumulative
#-------------------------------

df_years_all[materialstrings] = df_years_all[materialstrings].cumsum()

# Plot the cumulative values
df_years_all.plot(x="Publication Years", y=materialstrings, kind="line", figsize=(10, 6))

x_tick_list = [min(df_years_all['Publication Years'])] + [x for x in df_years_all['Publication Years'] if x%5==0] + [max(df_years_all['Publication Years'])]
x_tick_list = sorted(list(set(x_tick_list)))
plt.title('Cumulative Publication Years and Their Counts')
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
plt.close()