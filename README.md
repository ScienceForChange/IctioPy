# IctioPy
> Python3 data access library for [ictio.org](https://ictio.org)'s Citizen Observatory for Amazon basin fish observation.

This python module provides helper routines for citizen scientists that want to load and analyse data from Ictio's
citizen observatory for Amazon basin fish observation. The data from this Citizen Observatory is not freely available
via public API, but it can be downloaded as a zip file that is updated periodically after registration in web page.

## Features
This module takes an Ictio_Basic zip file from ictio.org and performs the following tasks on it:
- unzips its contents to a secure temporary folder
- flattens decompressed file and folder structure to make file paths more predictable
- autodetects the name of the observations file, which has a changing name based on the db generation date
- verifies the existence of "taxa" file, containing a taxonomy of species in Amazon basin
- loads observations and taxa files into dataframes
- combines information from both dataframes into one, so observations are complemented with species data
- sanitizes and curates the structure and the values 
- and returns a curated dataframe with all relevant data ready to be analysed

The structure of the dataframe is as follows:

**Observation related data:**

`obs_id`: Unique observation ID.

`user_id`: Anonymous, numeric ID of the user that made the observation.

`protocol_name`: Name of the observaton protocol used in the observation. Possible values: `During Fishing`, `After Fishing`, `Market Survey` and `Port Survey`

**Chronology related data:**

`obs_year`: Year of observation.

`obs_month`: Month of observation.

`obs_day`: Day of month of observation.

**Location related data:**

`watershed_code`: Unique identifier for watershed. For Ictio hotspots and personal locations, the watershed code and watershed name are inferred based on geographic position of Citizen Scientist at the time of observation.

`watershed_name`: Name of the watersed in which the osbervation was made.

`port`: This is the name of the port where data was collected and is only reported with the Port Protocol. This is not the location where fish were caught.

`location_type`: Ictio has three location types: Watersheds, Ictio Hotspots, and Personal Locations. This field will identify watersheds and Ictio Hotspots. This field will be null for personal locations. A personal location is any new location added with the upload tool or based on raw GPS coordinates.

`country_name`: Country in which the observation was made.

`state_province_name`: State/Province Code, automatically assigned by latitude and longitude. If there is a checklist assigned to a watershed, observation will be assigned to the State/Province where the centroid of the watershed is. If the watershed overlaps a boundary, it could be assigned to a different State/Province.

**Species related data:**

`taxon_code`: Species taxon code.

`scientific_name`: Scientific name of the species observed.

`category`: Category of the species observed<sup>*</sup>. 

`order1`: First order of the species observed<sup>*</sup>.

`family`: Family of the species observed<sup>*</sup>.

> <sup>*</sup>This data does not come from observations table. It is pulled from the separate taxa table that comes 
> embedded in Ictio_basic zip file. The value of `taxon_code` (present in both tables) is used to perform value lookup.  

**Fishing related data:**

`complete_checklist`: Indicates if the checklist was completed. A complete checklist is when all taxa caught during the fishing effort are reported. In a market survey it would be all taxa observed at the market. If observation was made via app, it is assumed that user reported a complete checklist.

`number_of_fish`: Number of individual fish reported for the given taxon.

`weight`: Total weight in Kg reported for the given taxon.

`price_local_currency`: Price per Kg in the local currency for the taxon.

`fishing_duration`: The duration of the fishing effort in hours.

`num_of_fishers`: Number of fishers participating in fishing effort.

> NOTE: At the time of this writing (May 2022), the ictio.org's observation database contains +86.400 observations. 
> Please bear in mind that processing the data can take more than 10 seconds. Your mileage may vary.

## Installation
as usual:
```
pip install ictiopy
```
## Usage
- First, register and accout at ictio.org (don't forget to read [terms of use](https://ictio.org/public/Ictio_data_terms_en.pdf)).
- Second, [download data](https://ictio.org/download) and store zip file locally in your hard disk.
- Finally, use this code in order to obtain a ready to use Pandas dataframe with Ictio's observation data:
```
import ictiopy
pandas_dataframe = ictiopy.load_zipdb('path/to/Ictio_Basic_yyyymmdd.zip') 
```
## About Ictio.org
Ictio.org is a project of [The Cornell Lab of Ornitology](https://www.birds.cornell.edu/home). 
Please, read [Ictio's terms of use](https://github.com/ScienceForChange/IctioPy/blob/master/ICTIO_ORG_LICENSE.md) before using its data.

## About MECODA and COS4CLOUD
This data parsing library has been specifically developed for [MECODA](https://github.com/eosc-cos4cloud/mecoda-orange), 
a toolkit built around [Orange Data Mining](https://orangedatamining.com/) for Citizen Observatory data analysis.

MECODA is part of the technological services for Citizen Observatories that are developed in the context of 
[COS4CLOUD](https://cos4cloud-eosc.eu/) project, funded by the European Union’s Horizon 2020 research and innovation 
programme under grant agreement #863463.    

## About Science for Change
If you want to tackle a societal problem that requires data to be gathered and analysed, you can count on 
Science for Change for designing, developing, creating a community around, or leverage data from a Citizen Observatory.
[Contact Science for Change](mailto://hello@scienceforchange.eu) for an evaluation of your case.
