import mechanicalsoup
import pandas as pd
import sqlite3




# Browser object
browser = mechanicalsoup.StatefulBrowser()

browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# Extract table headers (with tags and all info)

th = browser.page.find_all("th", attrs={"class": "table-rh"})

# Extract only the text
distribution = [value.text for value in th]
# ['AlmaLinux\n', 'Alpine Linux\n', 'ALT Linux\n',.....]

# Replace \n in every element
distribution = [value.replace("\n", "") for value in distribution]
# ['AlmaLinux', 'Alpine Linux', 'ALT Linux....]


# There is more than 1 table in the page, so we need to find the index of ZorinOS, the last on the first table
#print(distribution.index("Zorin OS"))
# 97

# We slice distribution
distribution = distribution[:98]

# Now the other columns
td = browser.page.find_all("td")

columns =[value.text.replace("\n", "") for value in td]

# We need to find the correct indexes
# For the end index we use Binary blobs, because "Active" is too common. Binary blobs is the next index.
#print(columns.index("AlmaLinux Foundation"))
# 6
#print(columns.index("Binary blobs"))
# 1084
columns = columns[6:1084]
#print(columns)

# Table as list of lists (not the same way as the tutorial)
table = []
while columns != []:
    row = []
    for i in range(11):
        row.append(columns[i])
    columns = columns[11:]
    table.append(row)

    
column_names = [
    "Founder",
    "Maintainer",
    "Initial_release_year",
    "Current_stable_version",
    "Security_updates_(years)",
    "Release_date",
    "System_distribution_commitment",
    "Forked_from",
    "Target_audience",
    "Cost", 
    "Status"
]
dictionary = {"Distribution": distribution}

for i in range(11):
    dictionary[column_names[i]] = [element[i] for element in table]


# Get data in dataframe
df = pd.DataFrame(data=dictionary)

# Insert data into database
connection = sqlite3.connect("linux_distro.db") 
cursor = connection.cursor()


cursor.execute(f"create table if not exists linux {tuple(df.columns)}")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])


connection.commit()
# Now ready for querys
""" cursor.execute("select founder from linux where founder = 'AlmaLinux Foundation';")
results = cursor.fetchall() 
print(results) """
connection.close()


