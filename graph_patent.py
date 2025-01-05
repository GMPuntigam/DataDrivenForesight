import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MultipleLocator
# Load the data files
dirname = os.path.dirname(__file__)

countries_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_countries.xlsx')
years_file = os.path.join(dirname, 'data', 'PatentSearch', 'Espacenet', 'Polymer_years.xlsx')

countries_data = pd.read_excel(countries_file)
publication_data = pd.read_excel(years_file)

    # Plot data for "Countries (family)"
plt.figure(figsize=(10, 6))
plt.bar(countries_data['Countries (family)'], countries_data['Number of documents'], color='skyblue')
plt.xlabel('Country')
plt.ylabel('Count')
plt.title('Patent Families by Country')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Plot data for "Earliest publication date (family)"
plt.figure(figsize=(10, 6))
plt.plot(publication_data['Earliest publication date (family)'], publication_data['Number of documents'], marker='o', color='orange')
plt.xlabel('Earliest Publication Date')
plt.ylabel('Count')
plt.title('Earliest Publication Date (Family)')
plt.gca().xaxis.set_major_locator(MultipleLocator(5))  # Adjust tick frequency if needed
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()