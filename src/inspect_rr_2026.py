import os
import pandas as pd

base = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition\6af458274c1e8_data_pack\Data Pack"
mapping = pd.read_csv(os.path.join(base, "competition_team_player_mapping.csv"))
rr_mapping = mapping[mapping['team_name'].str.contains("Rajasthan Royals", case=False, na=False)]
print("Unique RR competitions in mapping:")
print(rr_mapping[['comp_id', 'comp_name']].drop_duplicates())

print("\nSample RR players mapped in 2026 or latest:")
print(rr_mapping[['player_id', 'player_name', 'comp_name']].drop_duplicates().head(30))
