from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Read the CSV file
nypd_df = pd.read_csv('nypd_dataset.csv', header=0, low_memory=False)

# remove all unnecessary columns
features_to_drop = ['ADDR_PCT_CD', 'CMPLNT_FR_TM', 'CMPLNT_TO_DT', 'CMPLNT_TO_TM', 'HADEVELOPT', 'HOUSING_PSA',
                    'JURISDICTION_CODE', 'JURIS_DESC', 'KY_CD', 'LOC_OF_OCCUR_DESC', 'PARKS_NM', 'PD_CD', 'PD_DESC', 'RPT_DT',
                    'STATION_NAME', 'TRANSIT_DISTRICT', 'X_COORD_CD', 'Y_COORD_CD', 'Latitude', 'Longitude', 'Lat_Lon']
nypd_df.drop(features_to_drop, axis=1, inplace=True)

nypd_df['CMPLNT_FR_DT'] = pd.to_datetime(nypd_df['CMPLNT_FR_DT'], errors='coerce')
nypd_df = nypd_df.dropna(subset=['CMPLNT_FR_DT'])

# See the percentege of missing values in each variable
print((nypd_df.isna().sum()/nypd_df.shape[0]*100).sort_values(ascending=False))

# which borough has the most compaints
lab = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']     
complaints_per_neigh = nypd_df.groupby(["BORO_NM"]).count()["CMPLNT_NUM"].plot(kind='pie', y='points', autopct='%1.0f%%',
                                title='Total complaints made in each borough')
print(complaints_per_neigh)

plt.pie(complaints_per_neigh, labels = lab)
plt.show()


# becuase this dataset is extremely huge we will only work with data that is in recent dates and borough
nypd_df = nypd_df[(nypd_df['CMPLNT_FR_DT'] > '1/1/2019') & (nypd_df['BORO_NM'] == 'BROOKLYN')]
# # remove the CMPLNT_FR_DT column becasue we no longer need it
nypd_df.drop(['CMPLNT_FR_DT'], axis=1, inplace=True)

# # remove all the data that has na rows
nypd_df = nypd_df.dropna()

# # make all column to have str data type
nypd_df = nypd_df[:].astype(str)

# # print columns info
nypd_df.info()

nypd_df.to_csv("Pre_Processed_Dataset.csv", index = False)
