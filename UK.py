import pandas as pd
import altair as alt

death_database = pd.read_csv("deaths20222023.csv")
death_database = death_database.loc[:, ["Week number", "Total deaths England and Wales (2023)", "Total deaths England and Wales (2022)"]] 
death_database = death_database.dropna()
death_database = death_database.rename(columns={"Total deaths\nEngland and Wales (2023)": "Deaths 2023",
"Total deaths\nEngland and Wales (2022)" : "Deaths 2022"})
# death_database = death_database.set_index("Week number")

d2_database = pd.read_csv("deaths20202021.csv")
d2_database = d2_database.loc[:, ["Week number", "Care home resident deaths, all causes (2021)", "Care home resident deaths, all causes (2020)5"]] 
d2_database = d2_database.set_index("Week number")

death_database["Deaths 2021"] = d2_database["Care home resident deaths, all causes (2021)"].values
death_database["Deaths 2020"] = d2_database["Care home resident deaths, all causes (2020)5"].values

def get_quarter(week_number): 
    if 1 <= week_number <= 12:
        return "Q1"
    elif 13 <= week_number <= 25:
        return "Q2"
    elif 26 <= week_number <= 38:
        return "Q3"
    elif 39 <= week_number <= 52:
        return "Q4" 
    else:
        return "Error: week number out of range (1-52)"

assert get_quarter(1) == "Q1" 
assert get_quarter(15) == "Q2"
assert get_quarter(37) == "Q3"
assert get_quarter(51) == "Q4"
assert get_quarter(0) == "Error: week number out of range (1-52)" 
assert get_quarter(100) == "Error: week number out of range (1-52)"

death_database["Quarter"] = death_database["Week number"].apply(get_quarter)

death_database = death_database.drop(labels="Week number", axis="columns") 
death_database = death_database.set_index("Quarter")
# setting index twice because this way, the column "Week number" is automatically removed

# this gets rid of the commas in the values
death_database[["Deaths 2023", "Deaths 2022", "Deaths 2021", "Deaths 2020"]] = death_database[["Deaths 2023", "Deaths 2022", "Deaths 2021", "Deaths 2020"]].replace(",", "", regex=True)

# this converts all the numbers from string to integer
death_database[["Deaths 2023", "Deaths 2022", "Deaths 2021", "Deaths 2020"]] = death_database[["Deaths 2023", "Deaths 2022", "Deaths 2021", "Deaths 2020"]].astype(int)

# aggregates the data for each quarter
deaths = death_database.groupby(level=0).sum()

# need to reset index because altair cannot plot using index values 
deaths = deaths.reset_index()

gdp = pd.read_csv("gdp.csv")
gdp = gdp.rename(columns={'Title': 'Year', 'Gross Domestic Product: Quarter on Quarter growth: CVM SA %': 'GDP Percent Change'}) 
gdp = gdp[gdp['Year'].between('2020 Q1', '2023 Q4')]

# this code creates a new column "Quarter"; the values were formatted like "2020 Q1"
gdp["Quarter"] = gdp["Year"].str[-2:]

# this removes Q1/Q2/Q3/Q4 from the end of years
gdp['Year'] = gdp['Year'].str.replace(' Q1', '').str.replace(' Q2', '').str.replace(' Q3', '').str.replace(' Q4', '')

gdp = gdp.pivot(index='Quarter', columns='Year', values='GDP Percent Change') 
gdp.columns.name = None # gets rid of the 'Year' column
# 2023 Q4 has an NaN value because that information was not known when this datasheet was released

gdp = gdp.rename(columns={"2023": "GDP 2023", "2022": "GDP 2022", "2021": "GDP 2021", "2020": "GDP 2020"})
# this converts all the numbers from string to integer

gdp[["GDP 2020", "GDP 2021", "GDP 2022", "GDP 2023"]] = gdp[["GDP 2020", "GDP 2021", "GDP 2022", "GDP 2023"]].astype(float) 
gdp = gdp.reset_index()

# testing deaths dataset
assert deaths.loc[0, "Deaths 2023"] == 39064 
assert deaths.loc[1, "Deaths 2022"] == 31316 
assert deaths.loc[2, "Deaths 2021"] == 29537 
assert deaths.loc[3, "Deaths 2020"] == 37329

# testing gdp dataset
assert gdp.loc[0, "GDP 2023"] == 0.3 
assert gdp.loc[1, "GDP 2022"] == 0.1 
assert gdp.loc[2, "GDP 2021"] == 1.7 
assert gdp.loc[3, "GDP 2020"] == 1.4

# Plotting 2020 data
deaths2020 = alt.Chart(deaths).mark_line().encode(y=alt.Y("Deaths 2020").scale(domain=(0,65000)), x='Quarter')
deaths2020 = deaths2020.properties(width=400, height=300, title="2020 Death Count (per quarter)")
gdp2020 = alt.Chart(gdp).mark_line().encode(y=alt.Y("GDP 2020").scale(domain=(-22,18)), x='Quarter')
gdp2020 = gdp2020.properties(width=400, height=300, title="2020 GDP (per quarter)")
line = alt.Chart().mark_rule().encode(y=alt.datum(0))
chart2020 = deaths2020 | (gdp2020 + line)

# Plotting 2021 data
deaths2021 = alt.Chart(deaths).mark_line().encode(y=alt.Y("Deaths 2021").scale(domain=(0,45000)), x='Quarter')
deaths2021 = deaths2021.properties(width=400, height=300, title="2021 Death Count (per quarter)")
gdp2021 = alt.Chart(gdp).mark_line().encode(y=alt.Y("GDP 2021").scale(domain=(-2,8.5)), x='Quarter')
gdp2021 = gdp2021.properties(width=400, height=300, title="2021 GDP (per␣ ↪quarter)")
line = alt.Chart().mark_rule().encode(y=alt.datum(0))
chart2021 = deaths2021 | (gdp2021 + line)

# Plotting 2022 data
deaths2022 = alt.Chart(deaths).mark_line().encode(y=alt.Y("Deaths 2022").scale(domain=(0,40000)), x='Quarter')
deaths2022 = deaths2022.properties(width=400, height=300, title="2022 Death Count (per quarter)")
gdp2022 = alt.Chart(gdp).mark_line().encode(y=alt.Y("GDP 2022").scale(domain=(-0.2,0.6)), x='Quarter')
gdp2022 = gdp2022.properties(width=400, height=300, title="2022 GDP (per␣ ↪quarter)")
line = alt.Chart().mark_rule().encode(y=alt.datum(0))
chart2022 = deaths2022 | (gdp2022 + line)

# Plotting 2023 data
deaths2023 = alt.Chart(deaths).mark_line().encode(y=alt.Y("Deaths 2023").scale(domain=(0,41000)), x='Quarter')
deaths2023 = deaths2023.properties(width=400, height=300, title="2023 Death Count (per quarter)")
gdp2023 = alt.Chart(gdp).mark_line().encode(y=alt.Y("GDP 2023").scale(domain=(-0.2,0.4)), x='Quarter')
gdp2023 = gdp2023.properties(width=400, height=300, title="2023 GDP (per quarter)")
line = alt.Chart().mark_rule().encode(y=alt.datum(0))
chart2023 = deaths2023 | (gdp2023 + line)