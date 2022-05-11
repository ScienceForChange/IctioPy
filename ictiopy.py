#!env python3
import tempfile
import zipfile
from pathlib import Path
import pandas
import numpy as np

# The big database, which unfortunately has a changing name that we will have to infer on the go
ictio_bdb_file = 'BDB_????????.xlsx'


class SanityException(BaseException):
    pass


def unzip_db_to_folder(zipped_db_file, temp_folder):
    """
    Modified version of zipfile.extract_all that only extracts files that start with "BDB_", with no folder struct.
    This is needed because ictio's database contains a subfolder with ever changing name, as well as a
    BDB_????????.xlsx file that also changes name, making paths unpredictable.
    """
    import os
    import shutil
    with zipfile.ZipFile(zipped_db_file) as zip_file:
        dbfound = False
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            if os.path.basename(member).startswith('BDB_'):  # We just want the big observations database file
                source = zip_file.open(member)
                target = open(os.path.join(temp_folder, 'observations.xlsx'), "wb")  # we store with a predictable name
                with source, target:
                    shutil.copyfileobj(source, target)
                dbfound = True
            else:
                continue  # and we skip the rest
    if not dbfound:
        raise SanityException('Compressed zip file does not seem to have an observations file (BDB_########.xlsx)')


def load_ictio_bdb_file(data_folder, file_name):
    # REMEMBER: unlike the rest, the BDB file changes its name so it needs to be passed here as file_name
    """
    Pandas reading from excel (pandas.read_excel()) is really, really slow.
    We use FelixKling's alternative version in order to increase speed a bit.
    Programs using ictiopy will need to provide some sort of information message or warning, so the people waits a bit
    without falling into despair. Thanks to fast_excel.read, it's taking 10 secs in functional testing.
    """
    srcpath = str(Path(data_folder).joinpath(file_name))
    from fast_excel import read as fast_excel_read
    df = fast_excel_read(srcpath)
    return df


def sanitizedb(bdb):
    """
    Returns a pretty version of all the relevant data from BDB dataframe
    modifies dataframe INPLACE (return value can be used but it's not necessary)
    """
    # Change X by empty None in this field before casting to a nullable integer type
    bdb['number_of_fish'] = bdb['number_of_fish'].replace('x', None)
    # if you want integers and nulls at the same time in integer type columns, you need to cast them to Int64 type
    for column in ['number_of_fish', 'num_of_fishers']:
        bdb[column] = bdb[column].astype('Int64')
    # weight and price_local_currency are float
    for column in ['weight', 'price_local_currency']:
        bdb[column] = bdb[column].astype(float)
    # this is basically a structure assertion and a minor reordering
    bdb = bdb[['obs_id', 'weight', 'price_local_currency', 'obs_comments', 'upload_date_yyyymmdd',
               'num_photos', 'user_id', 'checklist_id', 'protocol_name', 'complete_checklist', 'fishing_duration',
               'submission_method', 'app_version', 'taxon_code', 'scientific_name', 'num_of_fishers', 'number_of_fish',
               'obs_year', 'obs_month', 'obs_day', 'port', 'location_type', 'country_code', 'country_name',
               'state_province_code', 'state_province_name', 'watershed_code', 'watershed_name']]
    bdb = bdb.replace(np.nan, None, regex=True)  # remove NANs changing them for None
    bdb = bdb.replace('', None, regex=True)  # remove empty strigns changing them for None
    bdb['protocol_name'] = bdb['protocol_name'].str.replace('CitSci for the Amazon - ', '')  # Shorter protocols
    bdb['complete_checklist'] = bdb['complete_checklist'].astype(bool)  # This field is boolean, not numeric
    return bdb


def load_zipdb(zipfilepath) -> object:
    data_folder = tempfile.mkdtemp()
    unzip_db_to_folder(zipfilepath, data_folder)
    bdb_data = load_ictio_bdb_file(data_folder, "observations.xlsx")  # WARNING: SLOW (almost 20 secs)
    return sanitizedb(bdb_data)


if __name__ == '__main__':
    print('Please, don\'t call this module directly. Use import and call load_zipdb() instead.')
    exit(1)
