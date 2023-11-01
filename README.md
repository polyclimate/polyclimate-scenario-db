Experimental test repo to run scenarios using the
[climate-assessment](https://github.com/iiasa/climate-assessment)
pipeline on GitHub Actions.

Input needs to be infilled scenarios with all needed gases
as the license status of the infilling database is unclear
whether it could be used in a repo like this.

2010 needs to have some values, see https://github.com/iiasa/climate-assessment/issues/21

When the scenario contains 2010 data it can be done manually with something like

```python
scenario.filter(year=2010).append(infilled_scenario).to_csv(filename_csv)

```

FaIR input is included in `data`.
Scenarios with unique filenames go into `scenario`.
Output data is saved in subdirectories in `output` based on the input scenario filename.

### References

FaIR calibration data:

Smith, C. (2022). FaIR v1.6.2 calibrated and constrained parameter set (v1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.6601980