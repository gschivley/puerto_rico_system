"Add O&M costs to existing generators using functions from PowerGenome"

from pathlib import Path
import pandas as pd

from powergenome.nrelatb import atb_fixed_var_om_existing, fetch_atb_heat_rates
from powergenome.util import init_pudl_connection

cwd = Path.cwd()
settings = {
    "capacity_col": "capacity_mw",
    "model_year": 2030,
    "target_usd_year": 2020,
    "atb_existing_year": 2020,
    "atb_data_year": 2022,
    "eia_atb_tech_map": {
        "Batteries": "Battery_*",
        "Biomass": "Biopower_Dedicated",
        "Solar Thermal without Energy Storage": "CSP_Class1",
        "Conventional Steam Coal": "Coal_newAvgCF",
        "Natural Gas Fired Combined Cycle": "NaturalGas_CCAvgCF",  # [NaturalGas_CCAvgCF, NETL_NGCC]
        "Combined Cycle": "NaturalGas_CCAvgCF",
        "Natural Gas Fired Combustion Turbine": "NaturalGas_CTAvgCF",
        "Combustion Turbine": "NaturalGas_CTAvgCF",
        "Petroleum Liquids": "NaturalGas_CTAvgCF",
        "Conventional Hydroelectric": "Hydropower_NSD4",
        "Natural Gas Internal Combustion Engine": "NaturalGas_CTAvgCF",
        "Petroleum Liquids with IC": "NaturalGas_CTAvgCF",
        "Landfill Gas": "NaturalGas_CTAvgCF",
        "Natural Gas Steam Turbine": "Coal_newAvgCF",
        "Onshore Wind Turbine": "LandbasedWind_Class4",
        "Solar Photovoltaic": "UtilityPV_Class1",
    },
}

tech_map = {
    "with CC": "Combined Cycle",
    "with ST": "Natural Gas Steam Turbine",
    "with GT": "Combustion Turbine",
}

pudl_engine, pudl_out, pg_engine = init_pudl_connection()
fn = cwd.parent / "data" / "existing_generators.csv"

gen_df = pd.read_csv(fn)
gen_df["operating_date"] = pd.to_datetime(gen_df["operating_date"])
gen_df["planned_retirement_date"] = pd.to_datetime(gen_df["planned_retirement_date"])
gen_df = gen_df.rename(columns={"plant_id": "plant_id_eia"})
for k, v in tech_map.items():
    gen_df.loc[gen_df["technology"].str.contains(k), "technology"] = v
atb_hr = fetch_atb_heat_rates(pg_engine, {"atb_data_year": 2022})

_gen_df = atb_fixed_var_om_existing(
    gen_df,
    atb_hr,
    settings,
    pg_engine,
    pd.DataFrame(columns=["plant_id_eia", "generator_id", "fgd"]),
)

final_df = pd.merge(
    gen_df,
    _gen_df[
        [
            "plant_id_eia",
            "generator_id",
            "Fixed_OM_Cost_per_MWhyr",
            "Fixed_OM_Cost_per_MWyr",
            "Var_OM_Cost_per_MWh",
        ]
    ],
    on=["plant_id_eia", "generator_id"],
)

final_df = final_df.rename(
    columns={
        "Fixed_OM_Cost_per_MWhyr": "fixed_o_m_mwh",
        "Fixed_OM_Cost_per_MWyr": "fixed_o_m_mw",
        "Var_OM_Cost_per_MWh": "variable_o_m_mwh",
    }
)

final_df.to_csv(
    cwd.parent / "system_inputs" / "existing_generators_with_om.csv",
    index=False,
    float_format="%g",
)
