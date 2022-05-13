# IctioPy
> Python3 data access library for [ictio.org](https://ictio.org)'s Citizen Observatory for Amazon basin fish observation.

This python module provides helper routines for citizen scientists that want to load and analyse data from Ictio's
citizen observatory for Amazon basin fish observation. The data from this Citizen Observatory is not freely available
via public API nor public download, but it can be downloaded as a zip file after registration in web page.

## Features
This module takes an Ictio_Basic zip file from ictio.org and performs the following tasks on it:
1. it detects the (unpredictable) path to the observations database file contained in it
2. it decompresses the file in a secure, temporary folder
3. loads observations files into a dataframe with an optimized version of pandas.read_excel
5. sanitizes and curates the structure and the values 
6. and returns a curated dataframe with all relevant data ready to be analysed

## Data structure

The structure of the dataframe is as follows:


- `obs_id`: Unique observation ID.
- `weight`: Total weight in Kg reported for the given taxon.
- `price_local_currency`: Price per Kg in the local currency for the taxon.
- `obs_comments`: Comments made by the Citizen Scientist at the time of registering the observation.
- `upload_date_yyyymmdd`: Date of observation upload. It does not necessarily match observation date. The relevant data for analysis purposes is the observation date.
- `num_photos`: Number of photos taken with the observation. The photos are not available in the basic version of the ictio.org's database, so this field is only included as a reference.
- `user_id`: Anonymous, numeric ID of the user that made the observation.
- `checklist_id`: Unique checklist identifier
- `protocol_name`: Name of the observation protocol used. Possible values: `During fishing event `, `After the fishing event`, `Market Survey` and `Port Survey`.
- `complete_checklist`: Indicates if the checklist was completed. A complete checklist is when all taxa caught during the fishing effort are reported. In a market survey it would be all taxa observed at the market. If observation was made via app, it is assumed that user reported a complete checklist.
- `fishing_duration`: The duration of the fishing effort in hours.
- `submission_method`: How was data submitted? `EFISH_android` for mobile app or `EFISH_upload` for upload tool.
- `app_version`: Version of the mobile app or upload tool used.
- `taxon_code`: Species taxon code.
- `scientific_name`: Scientific name of the species observed.
- `num_of_fishers`: Number of fishers participating in fishing effort.
- `number_of_fish`: Number of individual fish reported for the given taxon.
- `obs_year`: Year of observation.
- `obs_month`: Month of observation.
- `obs_day`: Day of month of observation.
- `port`: This is the name of the port where data was collected and is only reported with the Port Protocol. This is not the location where fish were caught.
- `location_type`: Ictio has three location types: Watersheds, Ictio Hotspots, and Personal Locations. This field will identify watersheds and Ictio Hotspots. This field will be null for personal locations. A personal location is any new location added with the upload tool or based on raw GPS coordinates.
- `country_code`: Country Code, automatically assigned by latitude and longitude. If you assign a checklist to a watershed it will be assigned to the country where the centroid of the watershed is. If the watershed overlaps a boundary, it could be assigned to a different country from where it is being submitted.
- `country_name`: Country in which the observation was made.
- `state_province_code`: State/Province Code, automatically assigned by latitude and longitude. If you assign a checklist to a watershed it will be assigned to the State/Province where the centroid of the watershed is. If the watershed overlaps a boundary, it could be assigned to a different State/Province.
- `state_province_name`: State/Province name, automatically assigned by latitude and longitude. If there is a checklist assigned to a watershed, observation will be assigned to the State/Province where the centroid of the watershed is. If the watershed overlaps a boundary, it could be assigned to a different State/Province.
- `watershed_code`: Unique identifier for watershed. For Ictio hotspots and personal locations, the watershed code and watershed name are inferred based on geographic position of Citizen Scientist at the time of observation.
- `watershed_name`: Name of the watersed in which the osbervation was made.

## PLEASE NOTE
> At the time of this writing (May 2022), the ictio.org's observation database contains +86.400 observations. 
> Please bear in mind that processing the data can take more than 10 seconds. Your mileage may vary.


## Installation
as usual:
```
pip install ictiopy
```
## Usage
- First, register an accout at ictio.org (don't forget to read [terms of use](https://ictio.org/public/Ictio_data_terms_en.pdf)).
- Second, [download data](https://ictio.org/download) and store zip file locally in your hard disk.
- Finally, use this code in order to obtain a ready to use Pandas dataframe with Ictio's observation data:
```
from ictiopy import ictiopy
pandas_dataframe = ictiopy.load_zipdb('path/to/Ictio_Basic_yyyymmdd.zip') 
```
## About Ictio.org
<img src="https://github.com/ScienceForChange/IctioPy/raw/master/ictio_org.png" alt="drawing" width="240px"/>

Ictio is a database and a mobile phone app created to register observations of caught fish in the Amazon basin. 
It was developed as part of the _Citizen Science for the Amazon_ project, which aims to connect citizens in the collection and sharing of information on the most important Amazonian fish species. Its wider objective is for that information to contribute in understanding Amazonian fish migration.

Ictio.org is a project of [The Cornell Lab of Ornitology](https://www.birds.cornell.edu/home). 
Please, read [Ictio's terms of use](https://github.com/ScienceForChange/IctioPy/blob/master/ICTIO_ORG_LICENSE.md) before using its data.

## About MECODA and COS4CLOUD
This data parsing library has been specifically developed for [MECODA](https://github.com/eosc-cos4cloud/mecoda-orange), 
a toolkit built around [Orange Data Mining](https://orangedatamining.com/) for Citizen Observatory data analysis.

MECODA is part of the technological services for Citizen Observatories that are developed in the context of 
[COS4CLOUD](https://cos4cloud-eosc.eu/) project, funded by the European Union’s Horizon 2020 research and innovation 
programme under grant agreement #863463.

Please visit [COS4CLOUD's web site](https://cos4cloud-eosc.eu) for more info on how COS4CLOUD empowers Citizen Science with technology and tools.

<img src="https://ec.europa.eu/info/sites/default/themes/europa/images/svg/logo/logo--en.svg" width="240px"/>
<img src="https://cos4cloud-eosc.eu/wp-content/uploads/2020/07/logo-cos4cloud-middle.png" width="240px"/>


## About Science for Change
<img src="https://www.scienceforchange.eu/wp-content/uploads/2021/06/Logos-SfC-color-2.png" width="240px"/>

If you want to tackle a social, environmental or health challenges that require data to be gathered and analysed, you can count on 
Science for Change for designing, developing, creating a community around, or leverage data from a Citizen Observatory.
[Contact Science for Change](mailto://hello@scienceforchange.eu) for an evaluation of your case.
