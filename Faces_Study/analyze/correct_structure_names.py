import os
import sys
from glob import glob
from data_conversion_util import *
learn_dir = os.path.join(os.getcwd(),'..','learning-task')
# import network structures from config.py file
sys.path.append(learn_dir)
from config import EDGES

# learning data directory
data_dir = os.path.join(learn_dir,'data')
data_fnames = glob(os.path.join(data_dir, "sub-???_sect-?.txt"))

# iterate through each data file
for f_full in data_fnames:
    # get basename of file
    f_base = os.path.basename(f_full)
    f_dir = os.path.dirname(f_full)
    f_full_csv = os.path.join(f_dir, f_base.split('.')[0]+'.csv')
    # set up text file in case need to write new text file
    # load header from file
    head_info = load_json(f_full,multiple_obj=True)[0]
    net_name = head_info["Structure"]
    # load structure from file
    net = load_json(f_full,multiple_obj=True)[1]
    # check which structure it matches
    for e in EDGES.keys():
        # convert EDGES into list of lists rather than list of tuples
        el = [list(elem) for elem in EDGES[e]]
        # if wrong in file, then move to orig and write out correct json
        if net == el and net_name != e:
            # change the head_info
            head_info["Structure"] = e
            # read in all lines of text file
            with open(f_full) as file:
                lines = file.readlines()
            # fix header information (first row)
            print("Changing first line of file "+f_base+" from")
            print(lines[0]) + "to"
            lines[0] = str(head_info)+"\n"
            print(lines[0])
            # write out text file again
            with open(f_full, "w") as f:
                f.writelines(lines)
            print(f_full+' saved')
            # convert to csv
            json2csv(json_file = f_full, csv_filename = f_full_csv)
            print(f_full_csv+' saved')
    # if this text file does not have a csv version, make one
    if not os.path.exists(f_full_csv):
        json2csv(json_file = f_full, csv_filename = f_full_csv)
        print(f_full_csv+' saved')

print("Done checking all files.")
