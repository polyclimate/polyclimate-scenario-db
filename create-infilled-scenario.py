# Add missing inputs to a scenario and do a test run.
# Requires a local copy of the infilling database file which is not included in this repo.

# Arguments:
#   input_scenario_filename output_scenario_filename

import warnings
import sys
import tempfile
from pathlib import Path

import pandas
import pyam
import pooch
from climate_assessment.cli import run_workflow

warnings.simplefilter(action="ignore", category=FutureWarning)

root = Path(__file__).parent

input_scenario_filepath = root / sys.argv[1]
output_scenario_filepath = root / sys.argv[2]

fair_slim_filename = "fair-1.6.2-wg3-params-slim.json"
fair_common_filename = "fair-1.6.2-wg3-params-common.json"

fair_slim_url = (
    "https://zenodo.org/record/6601980/files/fair-1.6.2-wg3-params-slim.json?download=1"
)
fair_slim_hash = "c071ca619c0ae37a6abdeb79c0cece7b"

pooch.retrieve(
    url=fair_slim_url,
    known_hash=f"md5:{fair_slim_hash}",
    path=root / "data",
    fname=fair_slim_filename,
)

fair_common_url = "https://zenodo.org/record/6601980/files/fair-1.6.2-wg3-params-common.json?download=1"
fair_common_hash = "42ccaffcd3dea88edfca77da0cd5789b"

pooch.retrieve(
    url=fair_common_url,
    known_hash=f"md5:{fair_common_hash}",
    path=root / "data",
    fname=fair_common_filename,
)

model = "fair"
model_version = "1.6.2"
fair_extra_config = root / "data" / fair_common_filename
probabilistic_file = root / "data" / fair_slim_filename

# Use fewer (e.g. 10) for a test run, this will break the
# the stats of the probabilistic ensemble
num_cfgs = 1

scenario_batch_size = 1

input_emissions_file = str(input_scenario_filepath)

infilling_database_file = str(
    root
    / "data"
    / "1652361598937-ar6_emissions_vetted_infillerdatabase_10.5281-zenodo.6390768.csv"
)

with tempfile.TemporaryDirectory() as outdir:
    run_workflow(
        input_emissions_file,
        outdir,
        model=model,
        model_version=model_version,
        probabilistic_file=probabilistic_file,
        fair_extra_config=fair_extra_config,
        num_cfgs=num_cfgs,
        infilling_database=infilling_database_file,
        scenario_batch_size=scenario_batch_size,
        harmonize=True,
    )

    infilled_scenario = pandas.read_csv(
        f"{outdir}/{input_scenario_filepath.stem}_harmonized_infilled.csv"
    )
    infilled_scenario["Variable"] = infilled_scenario["Variable"].apply(
        lambda x: x.replace("AR6 climate diagnostics|Infilled|", "")
    )
    # Drop duplicated rows (once as 'Harmonized', once as 'Emissions')
    infilled_scenario = infilled_scenario[
        ~infilled_scenario.Variable.str.contains("AR6 climate diagnostics")
    ]

    input_scenario = pyam.IamDataFrame(input_scenario_filepath)
    input_scenario.filter(year=2010).append(
        pyam.IamDataFrame(infilled_scenario)
    ).to_csv(output_scenario_filepath)
