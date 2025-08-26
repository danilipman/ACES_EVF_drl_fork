import os, glob, psutil
import numpy as np
from astropy.table import Table

local_path = '/Users/danilipman/Documents/Research/UConn/ACES_EVF/'
CS_cubes_path = '/Users/danilipman/Documents/Research/UConn/ACES_EVF/CS21/'

EVF_tab = Table.read(local_path + 'HVCC_resampled_subcube_regions.ecsv')
EVF_tab.sort('l') #sort the table by longitude 
ID_digit_list = ["%03d" % i for i in range(222)] #creates doubles with 000 digits for ID nubmers
EVF_tab.add_column(ID_digit_list, index=0, name ='New ID Number') #add the new column to the table

#Save the new version of the table 
EVF_tab.write("./HVCC_resampled_subcube_regions_newIDs.ecsv", format = 'ascii.ecsv', overwrite=True)

##Open the files and rename them according to the New ID Number column
for file in glob.glob(CS_cubes_path + '*EVF_*.fits', recursive=True):
    CS_cube = file
    Old_ID_num = int(os.path.basename(file).split('_',2)[1])
    EVF_filename = os.path.basename(file).split('_',2)[2].split('.fits',1)[0]

    Old_ID_index = np.where(EVF_tab['ID Number']==Old_ID_num)[0][0]
    matched_newID = EVF_tab['New ID Number'][Old_ID_index]

    newFilename = CS_cubes_path+'EVF_{}_{}.fits'.format(matched_newID, EVF_filename)

    os.rename(CS_cube,newFilename)
