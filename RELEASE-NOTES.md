Release Notes
=============

XXXX: Version 1.15
------------------
- added interactive installer script
- added missing libraries to pip requirements
- removed duplicate rows in school locations
- changed open_date in school locations to an integer to work around folium issue mapping DateTime
- updated school demographics with the latest data set
- updated data files on G drive
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