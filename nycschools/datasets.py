# NYC School Data
# Copyright (C) 2022-23. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU AFFERO GENERAL PUBLIC LICENSE (the "License") as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================


# these are the URLs into the open data portals
# update when new datasets are released
urls = {
    "datasite": {
        "url": "https://data.mixi.nyc/",
        "desc": "online data portal for nycschools"
    },
    "docbook": {
        "url": "https://adelphi-ed-tech.github.io/nycschools/install.html"
    },
    "snapshots": {
        "desc": "school snapshots scraped from DOE portal",
        "filename": "snapshot.feather",
        "rank_filename": "school-rankings.csv",
        "raw_snapshot": "snapshot-raw.csv"
    },
    "galaxy": {
        "url": "https://www.nycenet.edu/offices/d_chanc_oper/budget/dbor/galaxy/galaxyallocation/default.aspx",
        "desc": "Galaxy Budget Summaries",
        "url_stem": "https://www.nycenet.edu/offices/d_chanc_oper/budget/dbor/galaxy/galaxybudgetsummaryto/default.aspx?DDBSSS_INPUT=",
        "filename": "galaxy-budget.csv"
    },
    "cep": {
        "url": "https://www.iplanportal.com/",
        "desc": "Capital Expenditure Plan",
        "url_stem": "https://www.nycenet.edu/documents/oaosi/cep/2022-23/"
    },
    "school-data-archive": {
        "url": "https://drive.google.com/uc?export=download&id=1I35Wr1-UObcPm9CYSgqPUa8JOzOuAQBF",
        "filename": "nycschools-data.7z",
        "desc": "Download the archive of clean school data from public Google Drive"
    },
    "hs_admissions": {
        "url": "https://data.cityofnewyork.us/browse?q=Selection%20Criteria%20for%20High%20School%20Admissions",
        "data_urls": {
            "2018": "",
            "2019": "",
            "2020": "",
            "2021": "https://data.cityofnewyork.us/resource/9gs9-zhxw.csv?$limit=1000000"
        }
    },
    "hs_directory": {
        "url": "https://data.cityofnewyork.us/resource/97mf-9njv.csv?$limit=1000000",
        "desc": "High School Directories",
        "data_urls": {
            "2013": "https://data.cityofnewyork.us/resource/u553-m549.csv?$limit=1000000",
            "2014": "https://data.cityofnewyork.us/resource/n3p6-zve2.csv?$limit=1000000",
            "2015": "https://data.cityofnewyork.us/resource/by6m-6zpb.csv?$limit=1000000",
            "2016": "https://data.cityofnewyork.us/resource/7crd-d9xh.csv?$limit=1000000",
            "2017": "https://data.cityofnewyork.us/resource/s3k6-pzi2.csv?$limit=1000000",
            "2018": "https://data.cityofnewyork.us/resource/vw9i-7mzq.csv?$limit=1000000",
            "2019": "https://data.cityofnewyork.us/resource/uq7m-95z8.csv?$limit=1000000",
            "2020": "https://data.cityofnewyork.us/resource/23z9-6uk9.csv?$limit=1000000",
            "2021": "https://data.cityofnewyork.us/resource/8b6c-7uty.csv?$limit=1000000"
        }

    },
    "shsat_apps": {
        "url": "https://data.cityofnewyork.us/browse?q=SHSAT%20Admissions%20Test%20Offers%20By%20Sending%20School&sortBy=relevance",
        "filename": "shsat-applicants.csv",
        "desc": "SHSAT Applicants by School",
        "data_urls": {
            "2015": "https://data.cityofnewyork.us/resource/xqx4-kdvp.csv?$limit=1000000",
            "2016": "https://data.cityofnewyork.us/resource/8ws3-956v.csv?$limit=1000000",
            "2017": "https://data.cityofnewyork.us/resource/vsgi-eeb5.csv?$limit=1000000",
            "2018": "https://data.cityofnewyork.us/resource/uf53-ree9.csv?$limit=1000000",
            "2019": "https://data.cityofnewyork.us/resource/xuij-x4t4.csv?$limit=1000000",
            "2020": "https://data.cityofnewyork.us/resource/k8ah-28f4.csv?$limit=1000000"
        }
    },
    "zipcodes": {
        "filename": "zipcodes.geojson",
        "desc": "Load the zipcode boundaries from NYC Open Data Portal (via USPS)"
    },
    "demographics": {
        "url": "https://infohub.nyced.org/reports/students-and-schools/school-quality/information-and-data-overview",
        "data_urls": {
            "2023": "https://infohub.nyced.org/docs/default-source/default-document-library/demographic-snapshot-2019-20-to-2023-24-public.xlsx",
            # "2022": "https://infohub.nyced.org/docs/default-source/default-document-library/demographic-snapshot-2018-19-to-2022-23-(public).xlsx",
            "2022": "https://data.cityofnewyork.us/api/views/c7ru-d68s/files/7619cd06-7db2-4c98-9d9e-abfe186c169d?download=true&filename=Demographic%20Snapshot%202017-18%20to%202021-22%20(Public).xlsx",
            "2016": "https://data.cityofnewyork.us/resource/vmmu-wj3w.csv?$limit=1000000",
            "2013": "https://data.cityofnewyork.us/resource/s52a-8aq6.csv?$limit=1000000",
            "2006": "https://data.cityofnewyork.us/resource/ihfw-zy9j.csv?$limit=1000000",
        },
        "filename": "school-demographics.csv",
        "desc": "School demographic data from NYC Open Data Portal"
    },
    "class_size": {
        "url": "https://data.cityofnewyork.us/browse?q=Average%20Class%20Size%20by%20School&sortBy=relevance",
        "data_urls": {
            "2022": "https://infohub.nyced.org/docs/default-source/default-document-library/updated2023_avg_classsize_schl.xlsx",
            "2021": "https://data.cityofnewyork.us/resource/sgr7-hhwp.csv?$limit=1000000",
        },
        "filename": "school-class-size.csv",
        "filename_ptr": "ptr.csv",
        "desc": "Average class size by school and academic year and pupil teacher ratio for 2022-23"
    },
    "doe_school_wwww": {
        "url": "https://www.schools.nyc.gov/schools/",
        "desc": "this is the root URL part for DOE official school websites"
    },
    "building_footprints": {
        "url": "https://data.cityofnewyork.us/resource/5zhs-2jue.geojson?$limit=1000000",
        "city_footprints_feather": "nyc-footprints.feather",
        "school_footprints_file": "school-building-footprints.geojson",
        "desc_url": "https://data.cityofnewyork.us/City-Government/Building-Footprints/5zhs-2jue/about_data",
        "desc": "NYC GEOJSON file with all building footprints",
    },
    "school_geo": {
        "url": "https://data.cityofnewyork.us/download/jfju-ynrr/application%2Fx-zip-compressed",
        # "url": "https://data.cityofnewyork.us/resource/a3nt-yts4.geojson?$limit=1000000",
        "desc": "location points with zipcodes: https://data.cityofnewyork.us/Education/School-Point-Locations/jfju-ynrr/about_data"
    },
    "school_locations": {
        "url": "https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000",
        "desc": "https://data.cityofnewyork.us/Education/2019-2020-School-Locations/wg9x-4ke6/about_data",
        "years": {
            2019:"https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000",
            2018: "https://data.cityofnewyork.us/resource/9ck8-hj3u.csv?$limit=1000000",
            2017: "https://data.cityofnewyork.us/resource/p6h4-mpyy.csv?$limit=1000000",
            2016: "https://data.cityofnewyork.us/resource/ahjc-fdu3.csv?$limit=1000000",
            2015: "https://data.cityofnewyork.us/resource/i4ni-6qin.csv?$limit=1000000",
            2014: "https://data.cityofnewyork.us/resource/fxs2-faah.csv?$limit=1000000",
            2013: "https://data.cityofnewyork.us/resource/ac4n-c5re.csv?$limit=1000000",
            2012: "https://data.cityofnewyork.us/resource/emnd-d8ba.csv?$limit=1000000",

        },
        "filename": "school_locations.geojson",
        "desc": "x,y geolocations and location meta data"
    },
    "district_geo": {
        # open data no longer hosts this?!
        # "url": "https://data.cityofnewyork.us/api/geospatial/r8nu-ymqj?method=export&format=GeoJSON",
        "filename": "nyc-school-districts.geojson",
        "desc": "shape file for school districts"
    },
    "neighborhoods": {
        "url": "https://data.cityofnewyork.us/api/geospatial/99bc-9p23?method=export&format=GeoJSON",
        "desc":"based on NYT map?: https://data.cityofnewyork.us/City-Government/Neighborhood-Names-GIS/99bc-9p23",
        "filename": "neighborhood-names.geojson",
        "districts_filename": "district-neighborhoods.csv",
        "desc": "point data with neighborhood names"
    },
    "charter_ela": {
        "url": "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000",
        "filename": "charter-ela.csv",
        "desc": "charter school 3-8 ELA results"
    },
    "charter_math": {
        "url": "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000",
        "filename": "charter-math.csv",
        "desc": "charter school 3-8 math results"
    },
    "nyc_ela": {
        "url": "https://infohub.nyced.org/docs/default-source/default-document-library/school-ela-results-2013-2023-(public).xlsx",
        "url_2019": "https://data.cityofnewyork.us/api/views/hvdr-xc2s/files/4db8f0e7-0150-4302-bed7-529c89efa225?download=true&filename=school-ela-results-2013-2019-(public).xlsx",
        "filename": "nyc-ela.csv",
        "desc": "excel file with non-charter school ELA test results with demographic categories"
    },
    "nyc_math": {
        "url": "https://infohub.nyced.org/docs/default-source/default-document-library/school-math-results-2013-2023-(public).xlsx",
        "url_2019": "https://data.cityofnewyork.us/api/views/365g-7jtb/files/17910cb0-8a62-4037-84b5-f0b4c2b3f71f?download=true&filename=school-math-results-2013-2019-(public).xlsx",
        "filename": "nyc-math.csv",
        "desc": "excel file with non-charter school math test results with demographic categories"
    },
    "nyc_regents": {
        "url": "https://data.cityofnewyork.us/api/views/2h3w-9uj9/files/ae520e30-953f-47a0-9654-c77900232236?download=true&filename=2014-15-to-2018-19-nyc-regents-overall-and-by-category---public%20(1).xlsx",
        "filename": "nyc-regents.csv",
        "desc": "regents exam results"
    },
    "nysed_math_ela": {
        "comment": "Each test year has its own URL, so this item doesn't match others in format",
        "url": "https://data.nysed.gov/downloads.php",
        "urls": [
            "https://data.nysed.gov/files/assessment/20-21/3-8-2020-21.zip",
            "https://data.nysed.gov/files/assessment/18-19/3-8-2018-19.zip",
            "https://data.nysed.gov/files/assessment/17-18/3-8-2017-18.zip",
            "https://data.nysed.gov/files/assessment/16-17/3-8-2016-17.zip",
            "https://data.nysed.gov/files/assessment/15-16/3-8-2015-16.zip"
        ],
        "filename": "nysed-exams.feather",
        "desc": "NYS grades 3-8 ELA and Math test in a .zip archive"
    }
}
