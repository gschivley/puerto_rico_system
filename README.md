# Puerto Rico system setup

This repo has source data, compiled data, and PowerGenome inputs for a Puerto Rico system. Note that some input data/parameters are estimates and may not reflect the actual Puerto Rico power system.

All technology types are represented by a single cluster per region.

## Included files/folders

Raw data are in the `data` folder. `bin` contains scripts to compile hourly load and calaculate O&M costs.

The settings files for PowerGenome are in `pg_settings`. Additional input files are in `system_inputs`. These input files contain:

- System setup (definition of cases)
- Existing generators
- Misc operating parameters for each technology type
- Region assignment for each plant
- Hourly demand for each region
- Transmission capacity and costs for transmission expansion
- Regional cost corrections for ATB plant costs

A `Settings` folder with GenX settings and a `Run.jl` file are also included in this repo.

