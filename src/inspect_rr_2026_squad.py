import os
import pandas as pd

base = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition\6af458274c1e8_data_pack\Data Pack"
mapping = pd.read_csv(os.path.join(base, "competition_team_player_mapping.csv"))
rr_2026 = mapping[(mapping['comp_id'] == 3298) & (mapping['team_name'].str.contains("Rajasthan Royals", case=False, na=False))]
print(f"Total RR players in IPL 2026 mapping: {len(rr_2026)}")
print(rr_2026[['player_id', 'player_name', 'team_name']])
