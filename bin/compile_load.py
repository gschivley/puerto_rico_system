from pathlib import Path

import numpy as np
import pandas as pd

cwd = Path.cwd()

fn = cwd.parent / "data" / "puerto-rico-demand-with-zones.xlsx"

data = pd.read_excel(
    fn, sheet_name="Forecast__Gross Demand-8760", skiprows=11, usecols="K:N"
)
data = data.astype(int)
data.columns = data.columns.str.capitalize()
data_utc = data.copy()
for col in data.columns:
    data_utc[col] = np.roll(data[col], 4)


data_utc_tidy = data_utc.stack().sort_index(level=-1).reset_index()
data_utc_tidy.columns = ["time_index", "region", "load_mw"]
data_utc_tidy["year"] = 2030
data_utc_tidy.to_csv(cwd.parent / "system_inputs" / "load_profiles_PR.csv", index=False)
