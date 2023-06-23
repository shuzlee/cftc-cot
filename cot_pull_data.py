# -*- coding: utf-8 -*-
""" CFTC Disaggregated Futures Report

    Data Source: https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/petroleum_lf080222.htm
    API Info: https://publicreporting.cftc.gov/stories/s/r4w3-av2u
        
    Purpose: Pull data using CFTC API, plot, and analyze
"""

# Third Party Libraries
import pandas as pd
from sodapy import Socrata

# Set client to the CFTC website
client = Socrata("publicreporting.cftc.gov", None)

# Dataset Identifiers:
# Legacy Futures Only Report: "6dca-aqww"
# Legacy Combined Report: "jun7-fc8e"
# Disaggregated Futures Only Report: "72hh-3qpy",
# Disaggregated Combined Report: "kh3c-gbw2"
# TFF Futures Only Report: "gpe5-46if"
# TFF Combined Report: "yw9f-hn96"
# Supplemental Report: "4zgm-a668"

# If you don't know the data then pull a sample of 2000 records
sample = client.get("6dca-aqww", limit=2000)
sample_df = pd.DataFrame.from_records(sample)
sample_col_names = sample_df.columns

# Return results from selected dataset as JSON from API
results = client.get("6dca-aqww", 
                     where="(cftc_contract_market_code == '067651') AND \
                            (report_date_as_yyyy_mm_dd >= '2020-01-01T00:00:00.000' AND \
                            report_date_as_yyyy_mm_dd <= '2023-06-30T00:00:00.000')",
                     order="report_date_as_yyyy_mm_dd")

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)

# Convert columns to numeric - find the numeric columns and only change those
col_names = pd.DataFrame(df.columns)
convert_begin = col_names[col_names[0] == 'open_interest_all'].index[0]
convert_end = col_names[col_names[0] == 'contract_units'].index[0]
convert_list = df.columns[convert_begin:convert_end]

for col in convert_list:
    df[col] = pd.to_numeric(df[col])


# Example of pulling multiple contracts
results1 = client.get("6dca-aqww", 
                     where="(cftc_contract_market_code == '067651' OR \
                            cftc_contract_market_code == '067411') AND \
                            (report_date_as_yyyy_mm_dd >= '2020-01-01T00:00:00.000' AND \
                            report_date_as_yyyy_mm_dd <= '2023-06-30T00:00:00.000')",
                     order="report_date_as_yyyy_mm_dd")
    
# Convert to pandas DataFrame
df1 = pd.DataFrame.from_records(results1)
    
# Example of pulling specific columns
results2 = client.get("6dca-aqww", select="id, \
                     market_and_exchange_names, \
                 	 report_date_as_yyyy_mm_dd, \
                     yyyy_report_week_ww, \
                     contract_market_name, \
                     cftc_contract_market_code, \
                     cftc_market_code, \
                     cftc_region_code, \
                     cftc_commodity_code, \
                     commodity_name, \
                     open_interest_all", 
                     where="(cftc_contract_market_code == '067651' OR \
                            cftc_contract_market_code == '067411') AND \
                            (report_date_as_yyyy_mm_dd >= '2020-01-01T00:00:00.000' AND \
                            report_date_as_yyyy_mm_dd <= '2023-06-30T00:00:00.000')",
                     order="report_date_as_yyyy_mm_dd")
    
# Convert to pandas DataFrame
df2 = pd.DataFrame.from_records(results2)