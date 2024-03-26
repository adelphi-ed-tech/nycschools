Release Notes
=============

March 26, 2024: Version 1.17
----------------------------
- added neighborhood names to geo
- added plotly to requirements
- fixed bug in random point color
- updated school snapshots

March 18, 2024: Version 1.16
----------------------------
- added snapshot data
- added interactive legend to `ui`

March 18, 2024: Version 1.15.3
------------------------------
- fixed bug in local data loading
- removed noisy print statements

March 18, 2024: Version 1.15
-----------------------------
- local data_dir no longer needed, can load from data.mixi.nyc
- updated data sets
- added seg package (alpha) for running D and H segregation indices
- added snapshot package with additional data
- map UI functions in ui package
- added interactive installer script
- added missing libraries to pip requirements
- removed duplicate rows in school locations
- changed open_date in school locations to an integer to work around folium issue mapping DateTime
- updated school demographics with the latest data set
- no longer using Google Drive for data
- added syntax to ui.popup to put sections in popup info for explore()
- **breaking change**: renamed eni_pct to eni



March 15: Version 1.14.1
------------------------
- bug fixes for regents exams
- added new data file for regents to G Drive

March 15: Version 1.14
----------------------
- Added Data
    - HS Directory data 2013-2021 added to `schools`
    - Galaxy budget summaries at the school level to `budgets`
    - SHSAT HS admissions offers to `shsat`
- zip code data added to `geo`
- added school type to school demographics data

March 1, 2023, Version 1.13
---------------------------
- Added class size data from NYC and NYSED
- Added SHSAT high school feeder school data
- Helper functions in `nyschsools.ui`
- Updated docs
- Bug fixes