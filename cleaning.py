import pandas as pd

# Load datasets
funds_df = pd.read_csv("RS_Session_250_AU186.csv")
project_df = pd.read_csv("Convergenceproject_Conservation.csv")
tourism_df = pd.read_csv("Tourism_Statistics_Since_1991_2.csv")
iti_df = pd.read_csv("SES_2007-08_enrl_tech_indus.csv")

# Clean headers if needed
funds_df.columns = ['Year', 'Funds_Allocated_Cr', 'Funds_Utilized_Cr']
tourism_df.columns = ['Year', 'Foreign_Tourist_Numbers', 'Earnings_Cr', 'Earnings_USD', 'Domestic_Tourist_Numbers']
iti_df.columns = ['State_UT', 'ITI_Count', 'Intake_Capacity']
