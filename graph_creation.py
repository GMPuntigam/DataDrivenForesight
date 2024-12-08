import pandas as pd
import os
import re
from matplotlib import pyplot as plt

dirname = os.path.dirname(__file__)
data_affiliation_path = os.path.join(dirname, r"data/affiliation with departments.txt")
# Read the file line by line
with open(data_affiliation_path, "r") as file:
    lines = file.readlines()

data = []

# Process each line
for i, line in enumerate(lines):
    # Strip extra whitespace and split the line
    if i % 2==0:
        parts = re.split(r'\s\s+', line.strip())
    else:
        department = line.strip()
        data.append([parts[0]] + [department] + parts[1:])

# Convert the processed data to a DataFrame
df_affiliation = pd.DataFrame(data, columns=["Affiliation", "Department", "Record Count", "% of 281"])
df_affiliation['Record Count'] = pd.to_numeric(df_affiliation['Record Count'], downcast='integer', errors='coerce')

df_affiliation["Concat_Affiliation"] = df_affiliation["Affiliation"] + " " + df_affiliation["Department"]
new_affiliations = []
new_departsments = []
for j, name in enumerate(df_affiliation["Concat_Affiliation"]):
    parts = name.split(" ")
    found = False
    for i, part in enumerate(parts):
        if part in ["Center","Division", "College", "School", "Faculty", "Academy", "Department", 'Shunde', 'Institute', 'State']:
            affiliation = " ".join(parts[:i])
            department = " ".join(parts[i:])
            new_affiliations.append(affiliation)
            new_departsments.append(department)
            # print(affiliation)
            # print(department)
            # print(" ")
            found=True
            break
    if not found:
        new_affiliations.append(df_affiliation["Affiliation"][j])
        new_departsments.append(df_affiliation["Department"][j])
        print("Not Rearranged:" )
        print(df_affiliation["Affiliation"][j])
        print(df_affiliation["Department"][j])
        print(" ")

df_affiliation["Affiliation_new"] = new_affiliations
df_affiliation["Department_new"] = new_departsments

unique_affiliations = df_affiliation['Affiliation_new'].unique()
unique_affiliations_count = [sum(df_affiliation[df_affiliation["Affiliation_new"] == a]['Record Count']) for a in unique_affiliations]

df_affiliation_unique = pd.DataFrame(
    {'Affiliation': unique_affiliations,
     'Record Count': unique_affiliations_count,
    })
df_affiliation_unique.sort_values("Record Count", inplace=True, ascending=False)


data_countries_path = os.path.join(dirname, r"data/countries.txt")
# Read the file line by line
with open(data_countries_path, "r") as file:
    lines = file.readlines()

data = []
# Process each line
for i, line in enumerate(lines):
    # Strip extra whitespace and split the line
    parts = re.split(r'\s\s+', line.strip())
    data.append(parts)

# Convert the processed data to a DataFrame
df_countries = pd.DataFrame(data, columns=["Countries/Regions", "Record Count", "% of 281"])
df_countries['Record Count'] = pd.to_numeric(df_countries['Record Count'], downcast='integer', errors='coerce')
df_countries.sort_values("Record Count", inplace=True, ascending=False)
data_years_path = os.path.join(dirname, r"data/years.txt")
# Read the file line by line
with open(data_years_path, "r") as file:
    lines = file.readlines()

data = []
# Process each line
for i, line in enumerate(lines):
    # Strip extra whitespace and split the line
    parts = re.split(r'\s\s+', line.strip())
    data.append(parts)

# Convert the processed data to a DataFrame
df_years = pd.DataFrame(data, columns=["Publication Years", "Record Count", "% of 281"])
df_years['Record Count'] = pd.to_numeric(df_years['Record Count'], downcast='integer', errors='coerce')
df_years.sort_values("Publication Years", inplace=True, ascending=True)
# df_years.sort_values("Record count", inplace=True)
# Display the DataFrame
# print(df_affiliation.head())
# print(df_countries.head())
# print(df_years.head())

ax = df_affiliation_unique.plot.bar(x="Affiliation", y="Record Count")
affiliation_plot_path = os.path.join(dirname, r"graphs/affiliation with departments")
ax.figure.set_figwidth(20)
ax.figure.subplots_adjust(bottom=0.4)
plt.savefig(affiliation_plot_path)
ax = df_countries.plot.bar(x="Countries/Regions", y="Record Count")
ax.figure.subplots_adjust(bottom=0.4)
countries_plot_path = os.path.join(dirname, r"graphs/countries")
plt.savefig(countries_plot_path)
ax = df_years.plot.bar(x="Publication Years", y="Record Count")
ax.figure.subplots_adjust(bottom=0.2)
years_plot_path = os.path.join(dirname, r"graphs/years")
plt.savefig(years_plot_path)