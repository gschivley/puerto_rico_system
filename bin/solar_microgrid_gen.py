"Copy resource variability from normal solar to solar microgrid"

from datetime import datetime

import pandas as pd
import numpy as np
from pathlib import Path

from typer import run

CWD = Path.cwd()


def main(folder: str, cf_multiplier: float = 1.0):
    """Copy utility scale CF to solar microgrids in the Generators_variability.csv file.
    Modify the CF values using the parameter cf_multiplier.

    Parameters
    ----------
    folder : str
        Name of the folder to look for files in.
    cf_multiplier : float, optional
        Hourly CF of utility solar will be multiplied by this value, by default 1.0

    Raises
    ------
    ValueError
        cf_multplier cannot be greater than 1
    """
    if CWD.stem == "bin":
        gen_var_files = list((CWD.parent / folder).rglob("Generators_variability.csv"))
    else:
        gen_var_files = list((CWD / folder).rglob("Generators_variability.csv"))

    if cf_multiplier > 1:
        raise ValueError(
            "The argument 'cf_multiplier' is used to reduce the capacity factor of solar "
            "microgrids relative to utility solar and must be less than or equal to 1. "
            f"You have provided the value '{cf_multiplier}'. If you want the CF of solar "
            "microgrids to be higher than utility solar you should edit the script "
            "'puerto_rico/bin/solar_microgrid_gen.py' to clip hourly CF greater than 1."
        )

    for f in gen_var_files:
        df = pd.read_csv(f)
        for region in ["North", "South", "East", "West"]:
            mg_col = f"{region}_microgrid_solar_moderate_0"
            solar = f"{region}_utilitypv_class1"
            solar_col = [c for c in df.columns if solar in c]
            solar_col = solar_col[0]
            df[mg_col] = df[solar_col] * cf_multiplier

        df.to_csv(f, index=False)
        edits_file = f.parent / "edits.txt"
        if edits_file.exists():
            with edits_file.open("a") as f:
                f.write(f"{datetime.now()}")
                f.write(
                    f"Solar microgrid CF is now utility solar multiplied by {cf_multiplier}\n"
                )
        else:
            with edits_file.open("w") as f:
                f.write(f"{datetime.now()}")
                f.write(
                    f"Solar microgrid CF is now utility solar multiplied by {cf_multiplier}\n"
                )


if __name__ == "__main__":
    run(main)
