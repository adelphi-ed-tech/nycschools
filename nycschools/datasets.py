# NYC School Data
# Copyright (C) 2022. Matthew X. Curinga
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
  "demographics": {
    "url": "https://data.cityofnewyork.us/resource/vmmu-wj3w.csv?$limit=1000000",
    "filename":"school-demographics.csv",
    "desc": "School demographic data from NYC Open Data Portal"
  },
  "class_size": {
    "url": "https://data.cityofnewyork.us/browse?q=Average%20Class%20Size%20by%20School&sortBy=relevance",
    "data_urls": {
        "2021": "https://data.cityofnewyork.us/resource/sgr7-hhwp.csv?$limit=1000000"
    },
    "filename":"school-class-size.csv",
    "desc": "Average class size by school and academic year"
  },
  "school_geo": {
    "url": "https://data.cityofnewyork.us/resource/a3nt-yts4.geojson?$limit=1000000",
    "filename":"school-zipcodes.geojson",
    "desc": "location points with zipcodes"
  },
  "school_locations": {
    "url": "https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000",
    "filename":"school-locations.csv",
    "desc": "x,y geolocations and location meta data"
  },
  "district_geo": {
    "url": "https://data.cityofnewyork.us/api/geospatial/r8nu-ymqj?method=export&format=GeoJSON",
    "filename":"district-shapes.geojson",
    "desc": "shape file for school districts"
  },
  "charter_ela": {
    "url": "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000",
    "filename":"charter-ela.csv",
    "desc": "charter school 3-8 ELA results"
  },
  "charter_math": {
    "url": "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000",
    "filename":"charter-math.csv",
    "desc": "charter school 3-8 math results"
  },
  "nyc_ela": {
    "url": "https://data.cityofnewyork.us/api/views/hvdr-xc2s/files/4db8f0e7-0150-4302-bed7-529c89efa225?download=true&filename=school-ela-results-2013-2019-(public).xlsx",
    "filename":"nyc-ela.csv",
    "desc": "excel file with non-charter school ELA test results with demographic categories"
  },
  "nyc_math": {
    "url": "https://data.cityofnewyork.us/api/views/365g-7jtb/files/17910cb0-8a62-4037-84b5-f0b4c2b3f71f?download=true&filename=school-math-results-2013-2019-(public).xlsx",
    "filename":"nyc-math.csv",
    "desc": "excel file with non-charter school math test results with demographic categories"
  },
  "nyc_regents": {
    "url": "https://data.cityofnewyork.us/api/views/2h3w-9uj9/files/ae520e30-953f-47a0-9654-c77900232236?download=true&filename=2014-15-to-2018-19-nyc-regents-overall-and-by-category---public%20(1).xlsx",
    "filename":"nyc-regents.csv",
    "desc": "regents exam results"
  },
  "nysed_math_ela": {
    "comment":"Each test year has its own URL, so this item doesn't match others in format",
    "url":"https://data.nysed.gov/downloads.php",
    "urls": [
      "https://data.nysed.gov/files/assessment/20-21/3-8-2020-21.zip",
      "https://data.nysed.gov/files/assessment/18-19/3-8-2018-19.zip",
      "https://data.nysed.gov/files/assessment/17-18/3-8-2017-18.zip",
      "https://data.nysed.gov/files/assessment/16-17/3-8-2016-17.zip",
      "https://data.nysed.gov/files/assessment/15-16/3-8-2015-16.zip"
    ],
    "filename":"nysed-exams.csv",
    "desc": "NYS grades 3-8 ELA and Math test in a .zip archive"
  }
}