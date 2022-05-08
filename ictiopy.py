#!env python3
import tempfile
import zipfile
from pathlib import Path
import pandas
import numpy as np

# Species taxonomy
ictio_taxa_file = 'Ictio_Taxa.csv'
# And the big database, which unfortunately has a changing name that we will have to infer on the go
ictio_bdb_file = 'BDB_????????.xlsx'


class SanityException(BaseException):
    pass


def unzip_db_to_folder(zipped_db_file, temp_folder):
    # Modified version of zipfile.extract_all that flattens the folder structure of zip file contents
    # This is needed because ictio's database contains a subfolder with ever changing name, making paths unpredictable
    import os
    import shutil
    with zipfile.ZipFile(zipped_db_file) as zip_file:
        files_list = []
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
            if os.path.basename(member).startswith('.'):  # omit some dotfile dirt that is present in ictio's database
                continue
            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = open(os.path.join(temp_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            files_list.append(os.path.basename(member))
    return files_list  # Just for information purposes. Can be dismissed.


def find_bdb_file(folder):
    import glob
    # search the name of the big db file
    found_ictio_bdb_file = None
    searching_bdb_file = glob.glob(str(Path(folder).joinpath(ictio_bdb_file)), recursive=False)
    if len(searching_bdb_file) == 0:
        print('ERROR: Data folder does not contain any observations file (BDB_########.xlsx)')
        return None
    if len(searching_bdb_file) > 1:  # unlikely to happen, that would be an weird error from ictio
        print('Warning: Compressed zip file seems to have more than one observations file (BDB_########.xlsx)')
        print('Returning the first file in lexicographic order.')
    found_ictio_bdb_file = searching_bdb_file[0]
    return found_ictio_bdb_file


def check_data_folder_sanity(unzipped_db_folder):
    # checks for the existence of well known static files that should be present in temp data folder
    # returns the name of the unpredictable, name changing file BDB_########.xlsx found there
    bdb_file = find_bdb_file(unzipped_db_folder)
    if bdb_file is None:
        raise SanityException('Compressed zip file does not seem to have an observations file (BDB_########.xlsx)')
    if not Path.is_file(Path(unzipped_db_folder).joinpath(ictio_taxa_file)):
        raise SanityException('Compressed zip file does not seem to have a taxonomy file (Ictio_Taxa.csv)')
    return bdb_file


def load_ictio_taxa_file(data_folder):
    return pandas.read_csv(Path(data_folder).joinpath(ictio_taxa_file), header=0)


def load_ictio_bdb_file(data_folder, file_name):
    # REMEMBER: unlike the rest, the BDB file changes its name so it needs to be passed here as file_name
    """
    Pandas reading from excel (pandas.read_excel()) is really, really slow.
    We use FelixKling's alternative version of (fast_excel.read) in order to increase speed a bit.
    Programs using ictiopy will need to provide some sort of information message or warning, so the people waits a bit
    without falling into despair. Thanks to fast_excel.read, it's taking 10 secs in functional testing.
    """
    srcpath = str(Path(data_folder).joinpath(file_name))
    import fast_excel
    df = fast_excel.read(srcpath)
    return df


def merge_and_clean(bdb, taxa):
    """
    Returns a pretty version of all the relevant data linked and flattened from BDB and TAXA dataframes
    it uses a relationship between them:
    observations.taxon_code <=> taxonomy.SPECIES_CODE
    """
    pretty_df = pandas.merge(bdb, taxa, how='left', left_on='taxon_code', right_on='SPECIES_CODE')
    # Change X by empty None in this field before casting to a nullable integer type
    pretty_df['number_of_fish'] = pretty_df['number_of_fish'].replace('x', None)
    # if you want integers and nulls at the same time in integer type columns, you need to cast them to Int64 type
    for column in ['number_of_fish', 'num_of_fishers']:
        pretty_df[column] = pretty_df[column].astype('Int64')
    # weight and price_local_currency are float
    for column in ['weight', 'price_local_currency']:
        pretty_df[column] = pretty_df[column].astype(float)
    pretty_df.columns = pretty_df.columns.str.lower()  # lowercase some fields like CATEGORY or FAMILY
    # pick relevant columns discarding some others
    pretty_df = pretty_df[['obs_id', 'user_id', 'obs_year', 'obs_month', 'obs_day', 'protocol_name',
                           'watershed_code', 'watershed_name', 'port', 'location_type', 'country_name',
                           'state_province_name', 'taxon_code', 'scientific_name', 'category', 'order1', 'family',
                           'complete_checklist', 'number_of_fish', 'weight', 'price_local_currency', 'fishing_duration',
                           'num_of_fishers']]
    pretty_df = pretty_df.replace(np.nan, None, regex=True)  # remove NANs changing them for None
    pretty_df = pretty_df.replace('', None, regex=True)  # remove empty strigns changing them for None
    pretty_df['protocol_name'] = pretty_df['protocol_name'].str.replace('CitSci for the Amazon - ', '')  # Shorter protocols
    pretty_df['complete_checklist'] = pretty_df['complete_checklist'].astype(bool)  # This field is boolean, not numeric
    return pretty_df


def load_ictiozipdb(zipfilepath) -> object:
    # Prepare folder
    data_folder = tempfile.mkdtemp()
    # Unzip with no folder structure, ignoring dotfiles... (very useful here)
    unzip_db_to_folder(zipfilepath, data_folder)
    # Check that zip contains necessary files, and detect the name of the changing one
    bdb_file = check_data_folder_sanity(data_folder)
    # Load taxa
    taxa_data = load_ictio_taxa_file(data_folder)
    # Load observations
    bdb_data = load_ictio_bdb_file(data_folder, bdb_file)  # WARNING: SLOW (almost 20 secs)
    # Merge them and prettify
    final_df = merge_and_clean(bdb_data, taxa_data)
    return final_df


if __name__ == '__main__':
    print('Please, don\'t call this module directly. Use import and call load_ictiozipdb() instead.')
    exit(1)
