import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.ticker import MaxNLocator
from butterflychart import butterfly_chart
# Load the data files
dirname = os.path.dirname(__file__)

def round_up_to_next_50(n):
        return math.ceil(n / 50) * 50

def color_bar_by_label(bars, labels, label_to_color, color="coral"):
    for bar, label in zip(bars, labels):
        if label == label_to_color:
            bar.set_color(color)

def read_wos_txt(file_path):
    #  Read the file into a DataFrame
    df = pd.read_csv(file_path, sep="\t", engine="python", header=0)
    df.columns = [colname.strip() for colname in df.columns]
    
    # Drop the "% of 10,494" column
    df.drop(columns=df.columns[2], inplace=True)

    # df["Record Count"] = df["Record Count"].fillna(0)
    # df["Record Count"] = pd.to_numeric(df["Record Count"], errors="coerce")
    # df["Record Count"] = df["Record Count"].fillna(0)
    # df = df.astype({"Record Count":'int'})

    # Reset index for ease of processing
    df.reset_index(drop=True, inplace=True)

    # Identify rows where "Record Count" is empty and handle affiliation merging
    rows_to_drop = []
    for i in range(1, len(df)):
        df.loc[i, "Record Count"] = df.loc[i, "Record Count"].strip()
        if df.loc[i, "Record Count"] == "":
            # Append the "Affiliations" of the current row to the previous row
            df.loc[i - 1, "Affiliations"] += f" {df.loc[i, 'Affiliations']}"
            rows_to_drop.append(i)
    
    # Drop the rows identified earlier
    df.drop(index=rows_to_drop, inplace=True)
    df = df.astype({"Record Count":'int'})
    # Reset the index again
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={"Record Count": "Count"}, inplace=True)
    return df


populations_file = os.path.join(dirname, r'data/populations.xlsx')  # data from https://www.census.gov/data-tools/demo/idb/#/table?dashboard_page=country&COUNTRY_YR_ANIM=2025&menu=tableViz, January 2025
data_populations = pd.read_excel(populations_file, header=1)
data_populations["Name"] = data_populations["Name"].str.upper()


materialstrings = ["polymer","metal","cement","ceramic"]
colors = ["C0", "C1", "C2", "C3"]
materialstring_to_color = {string: color for (color, string) in zip(colors, materialstrings)}


cutoffs_dict_upper = {"cement": 20, 
                      "polymer": 80,
                      "ceramic": 8,
                      "metal": 30}

cutoffs_dict_lower = {"cement": 6, 
                      "polymer": 15,
                      "ceramic": 2,
                      "metal": 8}

for materialstring in materialstrings:
    affiliations_file = os.path.join(dirname, r'data/aff_' + materialstring +'.txt') 
    countries_file = os.path.join(dirname, r'data/countries_' + materialstring +'_wos.xlsx')  
    countries_population_plot_path = os.path.join(dirname, r'graphs/countries_population_' + materialstring)  # Replace with your local file path
    affiliations_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'')  # Replace with your local file path
    affiliations_low_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'_low')  # Replace with your local file path
    affiliations_histogram_plot_path = os.path.join(dirname, r'graphs/affiliation_' + materialstring +'_histogram')  # Replace with your local file path
    countries_plot_path = os.path.join(dirname, r'graphs/countries_' + materialstring +'')  # Replace with your local file path
    countries_count_per_population_plot_path = os.path.join(dirname, r'graphs/countries_count_' + materialstring +'_per_population')  # Replace with your local file path
    butterfly_plot_path = os.path.join(dirname, r'graphs/butterfly_' + materialstring) 

    # Load the data into DataFrames
    
    data_affiliations = read_wos_txt(affiliations_file)
    data_countries = pd.read_excel(countries_file)
    uk_country_list = ["SCOTLAND", "NORTH IRELAND", "ENGLAND", "WALES"]
    for country in uk_country_list:
        if country not in data_countries["Countries/Regions"]:
            data_countries.loc[len(data_countries)] = [country, 0]

    # merge uk country values
    count = sum([list(data_countries[data_countries["Countries/Regions"] == country]["Count"])[0] for country in ["SCOTLAND", "NORTH IRELAND", "ENGLAND", "WALES"]]) - 20
    data_countries.loc[len(data_countries)] = ["UNITED KINGDOM", count]
    data_countries = data_countries[~data_countries["Countries/Regions"].isin(uk_country_list)]
    data_countries.sort_values("Count", inplace=True, ascending=False)
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

    # Exclude double namings of CAS
    exclude_affiliations = ['UNIVERSITY OF CHINESE ACADEMY OF SCIENCES CAS', 'UNIVERSITY OF SCIENCE TECHNOLOGY OF CHINA CAS']
    data_affiliations_filtered = data_affiliations_filtered[
    ~data_affiliations_filtered['Affiliations'].isin(exclude_affiliations)]

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

    populations_filtered_scalefactor = [1/pop  if pop != 0 else 0 for pop in populations_filtered]

    #-------------------------------
    # Plot affiliations bar chart
    #-------------------------------
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    bars = plt.barh(data_affiliations_filtered['Affiliations'], data_affiliations_filtered['Count'])
    plt.title(f'Institutes with most publications for {materialstring} materials') # (Excluding Counts below {cutoffs_dict_upper[materialstring]})
    plt.ylabel('Affiliations')
    plt.xlabel('Count')
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    # Remove the default y-axis labels
    ax.set_yticks([])
    color_bar_by_label(bars, data_affiliations_filtered['Affiliations'], "CHINESE ACADEMY OF SCIENCES", color="coral")
    color_bar_by_label(bars, data_affiliations_filtered['Affiliations'], "University of Science Technology of China CAS".upper(), color="coral")
    color_bar_by_label(bars, data_affiliations_filtered['Affiliations'], "University of Chinese Academy of Sciences CAS".upper(), color="coral")
    
    # Annotate each bar with its corresponding category label
    for bar, label, count in zip(bars, data_affiliations_filtered['Affiliations'], data_affiliations_filtered['Count']):
        y = bar.get_y() + bar.get_height() / 2  # Center the text vertically
        available_space_percent = count/max(data_affiliations_filtered['Count']) 
        x = bar.get_x() + 0.01*max(data_affiliations_filtered['Count']) + count
        ax.text(x, y, label, va='center', ha='left', color='Black', fontsize=8, weight='bold', backgroundcolor='none')
    plt.xlim(0, round_up_to_next_50(max(data_affiliations_filtered['Count'])*1.4))
    plt.tight_layout()
    plt.savefig(affiliations_plot_path)
    plt.close()
    

    #-------------------------------
    # Plot affiliations bar chart low numbers
    #-------------------------------
    # plt.figure(figsize=(10, 6))
    # plt.barh(data_affiliations_filtered_low['Affiliations'], data_affiliations_filtered_low['Count'])
    # plt.title(f'Affiliations and Their Counts (Excluding Counts above {cutoffs_dict_lower[materialstring]})')
    # plt.ylabel('Affiliations')
    # plt.xlabel('Count')

    # ax = plt.gca()
    # ax.grid(which='major', axis='x', linestyle='-')
    # ax.set_axisbelow(True)
    # plt.tight_layout()
    # plt.savefig(affiliations_low_plot_path)
    # plt.close()

    #-------------------------------
    # Plot affiliations histogram chart just numbers
    #-------------------------------
    plt.figure(figsize=(10, 6))
    bins = range(min(data_affiliations['Count']), max(data_affiliations['Count']) + 1, 1)
    plt.hist(data_affiliations['Count'], bins=bins, edgecolor='none', color=materialstring_to_color[materialstring], alpha=0.7)
    plt.title(f'Histogram for number of publications per Institute, material type {materialstring}')
    plt.ylabel('Number of Institues with Count')
    plt.xlabel('Publication Count')
    ax = plt.gca()
    ax.grid(which='major', axis='both', linestyle='-')
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(axis='y', which='major', color='black', width=1.5, length=0)
    ax.tick_params(axis='y', which='minor', color='black', width=1.5, length=0)
    ax.set_yscale('log')
    current_ticks = ax.get_xticks()
    current_labels = [tick.get_text() for tick in ax.get_xticklabels()]  # Retrieve the current labels

    # Adjust tick positions by adding 0.5
    new_ticks = [tick + 0.5 for tick in current_ticks]
    plt.xticks([1.5] + new_ticks, ["1"] + current_labels)
    ax.set_xlim(1, ax.get_xlim()[1])
    plt.tight_layout()
    plt.savefig(affiliations_histogram_plot_path)
    plt.close()


    #-------------------------------
    # Plot countries/regions bar chart
    #-------------------------------
    plt.figure(figsize=(10, 6))
    bars = plt.barh(data_countries_filtered['Countries/Regions'], data_countries_filtered['Count'])
    plt.title(f'Publications per Country (Limited to more than {cutoffs_dict_upper[materialstring]} publications)')
    plt.ylabel('Countries')
    plt.xlabel('Number of Publications')
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    color_bar_by_label(bars, data_countries_filtered['Countries/Regions'], "PEOPLES R CHINA", color="coral")
    color_bar_by_label(bars, data_countries_filtered['Countries/Regions'], "USA", color="coral")

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
    plt.title(f'Countries and Their Populations')
    plt.ylabel('Countries')
    plt.xlabel('Population')
    ax = plt.gca()
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.savefig(countries_population_plot_path)
    plt.close()

    #-------------------------------
    # Plot butterflychart
    #-------------------------------

    data = pd.DataFrame({
    'Population': populations_filtered,
    'Publications devided by Population': scaled_counts
    }, index=data_countries_filtered['Countries/Regions'])
    butterfly_chart(
    data,
    figsize=(20, 6),
    wspace=0.25,
    title=f'Countries Publication Count per Population (Excluding Counts {cutoffs_dict_upper[materialstring]} and Below)'
    )
    plt.savefig(butterfly_plot_path)
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
    # plt.figure(figsize=(10, 6))
    # plt.plot(data_countries['Count'], data_countries['Countries/Regions'])
    # plt.title('Publication counts per country')
    # plt.ylabel('Countries')
    # plt.xlabel('Count')
    # plt.tight_layout()
    # ax = plt.gca()
    # ax.grid(which='major', axis='x', linestyle='-')
    # ax2 = ax.twiny()
    # ax2.plot(populations, data_countries['Countries/Regions'], color ="red")
    # # ax2.set_xlim(ax.get_xlim())
    # ax.set_yticklabels([])
    # ax.set_axisbelow(True)
    # plt.savefig(countries_justnumbers_plot_path)
    # plt.close()

df_years_all = pd.DataFrame()
df_pub = pd.DataFrame() # This is for materials without differentiating

# Load the complete data set for materials without differentiation
all_file = os.path.join(dirname, r'data/years' +'_wos.xlsx')  
data_pub = pd.read_excel(all_file)
data_pub = data_pub.set_index("Publication Years")
df_pub = df_pub.join(data_pub, how="outer", rsuffix=f"_{materialstring}").fillna(0) if not df_pub.empty else data_pub

predictions = {}
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
df_pub = df_pub.reset_index()

#Remove 2025, unreliable data
df_years_all = df_years_all[df_years_all["Publication Years"]!= 2025]
df_pub = df_pub[df_pub["Publication Years"]!= 2025]

#reset column names 
df_years_all.columns = ["Publication Years"] + materialstrings
#df_pub.columns = ["Publication Years"]

years_plot_path = os.path.join(dirname, r'graphs/years') 
years_cululative_plot_path = os.path.join(dirname, r'graphs/years_cumulative')
pub_plot_path = os.path.join(dirname, r'graphs/pub') 
pub_cululative_plot_path = os.path.join(dirname, r'graphs/pub_cumulative')
#-------------------------------
# Plot publication years line chart
#-------------------------------

# plt.figure(figsize=(10, 6))
ax = df_years_all[df_years_all["Publication Years"] != 2024].plot(x="Publication Years", y=materialstrings,
        kind="line", figsize=(10, 6), color=colors, marker = 'o')
for i, materialstring in enumerate(materialstrings):
    plt.plot([2023, 2024], df_years_all[df_years_all["Publication Years"].isin([2023, 2024])][materialstring], linestyle='dashed', color=colors[i])

# for materialstring in materialstrings:
#     plt.plot(df_years_all['Publication Years'], df_years_all[materialstring])
x_tick_list = [min(df_years_all['Publication Years'])] + [x for x in range(min(df_years_all['Publication Years']), max(df_years_all['Publication Years'])) if x%5==0] + [max(df_years_all['Publication Years'])]
x_tick_list = sorted(list(set(x_tick_list)))
plt.title('Number of Publications per Year')
plt.xlabel('Year')
plt.ylabel('Publication Count')
plt.xticks(x_tick_list)
plt.minorticks_on()
plt.tight_layout()
ax.set_xlim(1980, 2024)
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.tick_params(axis='x', which='major', color='black', width=1.5, length=10)
ax.tick_params(axis='x', which='minor', color='black', width=1.5, length=5)
ax.grid(which='major', axis='y', linestyle='-')
ax.set_axisbelow(True)
plt.savefig(years_plot_path)
plt.close()

# All materials
plt.figure(figsize=(10, 6))
plt.plot(df_pub['Publication Years'], df_pub['Count'], marker = 'o')
plt.xlabel('Year')
plt.ylabel('Publication Count')
plt.title('Number of Publications per Year')
plt.grid(axis='y', linestyle='-', alpha=0.7)
years = range(min(df_pub['Publication Years']), max(df_pub['Publication Years']) + 2)
x_tick_list = [min(years)] + [x for x in years if x%5==0] + [max(years)]
x_tick_list = sorted(set(x_tick_list))

plt.xticks(x_tick_list, labels=x_tick_list, rotation=0)
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1)) 
ax.set_xlim(1980, 2025)

plt.tight_layout()
# plt.show()
plt.savefig(pub_plot_path)
plt.close()

#-------------------------------
# Plot publication years bar chart cumulative
#-------------------------------

# def func(x, a, b, c):
#     return a * np.exp(b * x) + c

# def func_render(x, a, b, c):
#     return a*0.8 * np.exp(b * x) + c
# from scipy.optimize import curve_fit

df_years_all[materialstrings] = df_years_all[materialstrings].cumsum()
for materialstring in materialstrings:
    # popt, pcov = curve_fit(func, df_years_all.index, df_years_all[materialstring])
    model = np.poly1d(np.polyfit(df_years_all.index, 
                                df_years_all[materialstring], 4)) 
    predictions[materialstring] = {"years": [2024, 2025, 2026, 2027], "counts": [list(df_years_all[materialstring])[-1], model(df_years_all.index[-1]+1), model(df_years_all.index[-1]+2), model(df_years_all.index[-1] +3)]}
    # predictions[materialstring] = {"years": [2024, 2025, 2026, 2027], "counts": [list(df_years_all[materialstring])[-1], func_render(df_years_all.index[-1]+1, *popt), func_render(df_years_all.index[-1]+2, *popt), func_render(df_years_all.index[-1] +3, *popt)]}

# Plot the cumulative values
df_years_all.plot(x="Publication Years", y=materialstrings, kind="line", figsize=(10, 6), color=colors)

x_tick_list = [min(df_years_all['Publication Years'])] + [x for x in range(min(df_years_all['Publication Years']), 2030) if x%5==0] + [2030]
x_tick_list = sorted(list(set(x_tick_list)))
plt.title('Cumulative Number of Publications')
plt.xlabel('Years')
plt.ylabel('Cumulative Publication Count')
plt.xticks(x_tick_list)
plt.minorticks_on()
plt.tight_layout()
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.tick_params(axis='x', which='major', color='black', width=1.5, length=10)
ax.tick_params(axis='x', which='minor', color='black', width=1.5, length=5)
ax.grid(which='major', axis='y', linestyle='-')
ax.set_axisbelow(True)
ax.set_xlim(1980, 2030)

for i,materialstring in enumerate(materialstrings):
    plt.plot(predictions[materialstring]["years"], predictions[materialstring]["counts"], linestyle='dashed', color=colors[i])

custom_line = Line2D([0], [0], color="grey", linestyle="--", label="forecast")
# Add the legend, including the custom line
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + [custom_line])

plt.savefig(years_cululative_plot_path)
plt.close()

# For all materials
df_pub = df_pub.sort_values('Publication Years')
df_pub.reset_index(drop=True)
df_pub['Count'] = df_pub['Count'].cumsum()
plt.figure(figsize=(10, 6))
plt.plot(df_pub['Publication Years'], df_pub['Count'], marker = 'o')
plt.xlabel('Year')
plt.ylabel('Cumulative Publication Count')
plt.title('Cumulative Number of Publications per Year')
plt.grid(axis='y', linestyle='-', alpha=0.7)

years = range(min(df_pub['Publication Years']), max(df_pub['Publication Years']) + 2)
x_tick_list = [min(years)] + [x for x in years if x%5==0] + [max(years)]
x_tick_list = sorted(set(x_tick_list))

plt.xticks(x_tick_list, labels=x_tick_list, rotation=0)
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1)) 
ax.set_xlim(1980, 2025)

plt.tight_layout()
# plt.show()
plt.savefig(pub_cululative_plot_path)
plt.close()

#-------------------------------
# Plot affiliations histogram chart stacked
#-------------------------------


hist_data = []
for materialstring in materialstrings:
    affiliations_file = os.path.join(dirname, r'data/aff_' + materialstring +'.txt') 
    data_affiliations = read_wos_txt(affiliations_file) 
    # data_affiliations = pd.read_excel(affiliations_file)
    # counts_of_counts = data_affiliations["Count"].value_counts()
    hist_data.append(data_affiliations["Count"])
#-------------------------------
plt.figure(figsize=(10, 6))
bins = range(min([hist_data[i].min() for i in range(len(hist_data))]), max([hist_data[i].max() for i in range(len(hist_data))]) + 1, 1)
for i, materialstring in zip(range(len(hist_data)), materialstrings):
    p = plt.hist(hist_data[i], bins=bins, edgecolor='none', color=materialstring_to_color[materialstring], alpha=0.5, stacked=False, label=materialstring)
plt.title(f'Stacked histogram for number of publications per Institute for all material types')
plt.legend(title="Materials")
plt.ylabel('Number of Institues with Count')
plt.xlabel('Publication Count')
ax = plt.gca()
ax.grid(which='major', axis='both', linestyle='-')
ax.set_axisbelow(True)
ax.set_xlim(1, 100)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.tick_params(axis='y', which='major', color='black', width=1.5, length=0)
ax.tick_params(axis='y', which='minor', color='black', width=1.5, length=0)
ax.set_yscale('log')
current_ticks = ax.get_xticks()
current_labels = [tick.get_text() for tick in ax.get_xticklabels()]  # Retrieve the current labels

#remove 0
current_ticks = current_ticks[1:]
current_labels = current_labels[1:]

# Adjust tick positions by adding 0.5
new_ticks = [tick + 0.5 for tick in current_ticks]
plt.xticks([1.5] + new_ticks, ["1"] + current_labels)

plt.tight_layout()
affiliations_histogram_stacked_plot_path = os.path.join(dirname, r'graphs/affiliation_histogram_stacked')
plt.savefig(affiliations_histogram_stacked_plot_path)
plt.close()