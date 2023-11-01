import warnings

from pathlib import Path
import pooch

from climate_assessment.cli import run_workflow

warnings.simplefilter(action="ignore", category=FutureWarning)

root = Path(__file__).parent

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
num_cfgs = 2237

scenario_batch_size = 1

for scenario in (root / "scenarios").glob("*.csv"):
    input_emissions_file = str(scenario)

    outdir = root / "output" / scenario.stem
    outdir.mkdir(parents=True, exist_ok=True)

    if (outdir / f"{scenario.stem}_IAMC_climateassessment0000.csv").exists():
        continue

    print("Processing scenario file:", scenario.name)

    run_workflow(
        input_emissions_file,
        outdir,
        model=model,
        model_version=model_version,
        probabilistic_file=probabilistic_file,
        fair_extra_config=fair_extra_config,
        num_cfgs=num_cfgs,
        infilling_database=None,
        scenario_batch_size=scenario_batch_size,
        harmonize=True,
    )
