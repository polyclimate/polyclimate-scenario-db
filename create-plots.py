import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pyam

plt.style.use("ggplot")

root = Path(__file__).parent

scenario_file = root / sys.argv[1]
scenario = pyam.IamDataFrame(scenario_file)
results = pyam.IamDataFrame(
    root
    / "output"
    / scenario_file.stem
    / f"{scenario_file.stem}_IAMC_climateassessment0000.csv"
)

fig, ax = plt.subplots(3, 1)

scenario.filter(variable="Emissions|CO2*").plot(ax=ax[0])
scenario.filter(variable="Emissions|CH4").plot(ax=ax[1], title="Emissions|CH4")
scenario.filter(variable="Emissions|N2O").plot(ax=ax[2], title="Emissions|N2O")
fig.tight_layout()

plt.savefig("scenario-emissions.png")

fig, ax = plt.subplots(3, 1)
results.filter(variable="Surface Temperature (GSAT)|FaIRv1.6.2|50.0th Percentile").plot(
    ax=ax[0], title="Surface Temperature (GSAT)|FaIRv1.6.2|50.0th Percentile"
)
results.filter(
    variable="Atmospheric Concentrations|CO2|FaIRv1.6.2|50.0th Percentile"
).plot(ax=ax[1], title="Atmospheric Conc.|CO2|FaIRv1.6.2|50.0th Prctl.")
results.filter(
    variable="Effective Radiative Forcing|Basket|Greenhouse Gases|FaIRv1.6.2|50.0th Percentile"
).plot(
    ax=ax[2],
    title="Eff. Radiative Forcing|Basket|GHG|FaIRv1.6.2|50.0th Prctl.",
)
fig.tight_layout()

plt.savefig("climate-assessment.png")
