import pandas as pd
import matplotlib.pyplot as plt
import math
import os
# Load the data files
dirname = os.path.dirname(__file__)
affiliations_file = os.path.join(dirname, r'data/affiliation.xlsx')  # Replace with your local file path
years_file = os.path.join(dirname, r'data/years.xlsx')  # Replace with your local file path
countries_file = os.path.join(dirname, r'data/countries.xlsx')  # Replace with your local file path

# Load the data into DataFrames
data_affiliations = pd.read_excel(affiliations_file)
data_years = pd.read_excel(years_file)
data_countries = pd.read_excel(countries_file)

# Exclude small counts if needed (4 and below for this example)
data_affiliations_filtered = data_affiliations[data_affiliations['Count'] > 4]
data_years_filtered = data_years  # No filtering applied here
data_countries_filtered = data_countries[data_countries['Count'] > 4]

# Plot affiliations bar chart
plt.figure(figsize=(10, 6))
plt.barh(data_affiliations_filtered['Affiliations'], data_affiliations_filtered['Count'])
plt.title('Affiliations and Their Counts (Excluding Counts 4 and Below)')
plt.ylabel('Affiliations')
plt.xlabel('Count')
ax = plt.gca()
ax.grid(which='major', axis='x', linestyle='-')
ax.set_axisbelow(True)
# y_tick_list = range(0, math.ceil(max(data_affiliations_filtered['Count']))+1, 2)
# plt.yticks(y_tick_list)
# plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Plot publication years bar chart
plt.figure(figsize=(10, 6))
plt.bar(data_years_filtered['Publication Years'], data_years_filtered['Count'])
x_tick_list = range(min(data_years_filtered['Publication Years']), math.ceil(max(data_years_filtered['Publication Years']))+1)
plt.title('Publication Years and Their Counts')
plt.xlabel('Publication Years')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.xticks(x_tick_list)
plt.tight_layout()
plt.show()

# Plot countries/regions bar chart
plt.figure(figsize=(10, 6))
plt.bar(data_countries_filtered['Countries/Regions'], data_countries_filtered['Count'])
plt.title('Countries/Regions and Their Counts (Excluding Counts 4 and Below)')
plt.xlabel('Countries/Regions')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()