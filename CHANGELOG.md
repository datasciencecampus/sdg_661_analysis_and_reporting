# Change Log

## REF
2022-01-26
- Updated [UK_Reporting](./UK_reporting.ipynb) notebook to provide a walkthrough.
- Added a [user guide](./Colab_Guide.md) for running the UK reporting workflow on Google Colab.
- Updated data sources to latest versions.
  - [Yearly History v1.3](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_3_YearlyHistory)
  - [Monthly History v1.3](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_3_MonthlyHistory)
- Replaced`filterDate` (in `GEE_extractor.py`) function as it relies on the `system:time_start` image property. This is not always available in the data so the filter operation now explicitly looks at the `year` image property.
