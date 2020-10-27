import os
from shutil import copy2 as cp
from data_conversion_util import *
import numpy as np
old_err_state = np.seterr(divide='raise')
ignored_states = np.seterr(**old_err_state)

data_dir = 'data/'
# copy files from original directory? Note: must specify directies below
copy_orig_files = False 
# overwrite files? Yes=True No=False
overwrite   = False 

# copy data files over
if copy_orig_files:
    data_dir = os.path.join(os.getcwd(),data_dir)
    orig_data_dir = '/Users/miriam/CSNLGoogleDrive/NetLearn/network-learning-master/data/'
    for file in os.listdir(orig_data_dir):
        if file.endswith(".txt"):
            orig_file_path = os.path.join(orig_data_dir, file)
            new_file_path = os.path.join(data_dir, file)
            if not os.path.isfile(new_file_path) or overwrite:
                print 'copying file '+ orig_file_path + ' to ' +new_file_path
                cp(orig_file_path,data_dir)


fname_out_summary = data_dir+'net-learn_accuracy.csv'

summary_csvlist = []
summary_csvlist.append(['subID','gender','age','section','mode','structure','condition','run','n_correct','n_total','perc_correct'])


sub_files=[]
for file in os.listdir(data_dir):
    if file.endswith(".txt"):
        sub_files.append(file)
        print 'loading file '+ os.path.join(data_dir, file)


for f in sub_files:
    subject_num = f.split('_')[0]

    fname_in  = data_dir+subject_num+'_1.txt'
    fname_out = data_dir+subject_num+'_1.csv'

    
    # read in file
    data_dict = load_json(fname_in,multiple_obj=True)
    
    # determine which of the two networks was seen
    if len(data_dict[1]) == 15:
    	structure='A'
    elif len(data_dict[1]) == 8:
    	structure='B'
    # extract subject info (same for every trial per participant)
    subinfo=[data_dict[0]['ID'],data_dict[0]['Gender'],data_dict[0]['Age'],data_dict[0]['Section'],data_dict[0]['Mode'],structure,data_dict[0]['NetworkType']]

    # initialize run count (for up to 10 runs)
    run_count = np.array([0,0,0,0,0,0,0,0,0,0])
    # initialize run accuracy count 
    run_correct = np.array([0,0,0,0,0,0,0,0,0,0])
    
    # check if file was already converted
    if os.path.isfile(fname_out) and not overwrite:
        print fname_out + ' already exists. Skipping data file.'
        # go through each row in data file
        for i in range(3,len(data_dict)):
            # r = all data from current row
            r=data_dict[i]
            # tindex = array(row,block,trial)
            tindex=r['trial_index'].split('.')
            if 'test' in r['trial_index']:
                run_num = int(tindex[0])
                run_count[run_num] += 1
                if r['correct']:
                    run_correct[run_num] += 1
        run_count = run_count[np.nonzero(run_count)]
        run_correct = run_correct[np.nonzero(run_count)]*1.
        run_accuracy = run_correct/run_count
        
        for r in range(len(run_count)):
             rlist = subinfo + [int(r),run_correct[r],run_count[r],run_accuracy[r]]
             summary_csvlist.append(rlist)
             
        continue
    else:
        print 'Converting ' + fname_in + ' to ' + fname_out   
    
    ## build csv file row by row
    # initialize 2D list
    data_csvlist = []
    # header for subject info
    data_csvlist.append(['subID','gender','age','section','mode','structure','condition','run','block','trial','connected','image1','image2','nodeIndex1','nodeIndex2','response','rt','correct'])
    
    
    # go through each row in data file
    for i in range(3,len(data_dict)):
        # r = all data from current row
        r=data_dict[i]
        # tindex = array(row,block,trial)
        tindex=r['trial_index'].split('.')
        # if training trial
        if 'train' in r['trial_index']:
             # t1 = trial showing connected alters
             t1 = int(tindex[-1])*2
             # t2 = trial showing unconnected alters
             t2 = int(tindex[-1])*2+1
             # image ID
             image1 = data_dict[2][str(r['image'])]
             # rlist = connected trial data
             rlist = subinfo + [tindex[0],'train',t1,True,image1,'NA',r['image'],'NA','NA',r['rt_connected'],'NA']
             # add connected trial data to write out
             data_csvlist.append(rlist)
             # rlist = uncconected trial data
             rlist = subinfo + [tindex[0],'train',t2,False,image1,'NA',r['image'],'NA','NA',r['rt_unconnected'],'NA']
             # add unconnected trial data to write out
             data_csvlist.append(rlist)
        # if test trial
        elif 'test' in r['trial_index']:
            # person 1
            nodeIndex1 = r['images'][0]
            # person 2
            nodeIndex2 = r['images'][1]
            # person 1's image
            image1 = data_dict[2][str(nodeIndex1)]
            # person 2's image
            image2 = data_dict[2][str(nodeIndex2)]
            # get participant's response
            if r['response'][0] == 'left':
                response = 'N'
            elif r['response'][0] == 'right':
                response = 'Y'
            # rlist = trial data
            rlist = subinfo + [tindex[0],'test',t1,r['connected'],image1,image2,nodeIndex1,nodeIndex2,response,r['response'][1],r['correct']]
            # add trial data to write out
            data_csvlist.append(rlist)
            
            run_num = int(tindex[0])
            run_count[run_num] += 1
            if r['correct']:
                run_correct[run_num] += 1
                 
    run_count = run_count[np.nonzero(run_count)]
    run_correct = run_correct[np.nonzero(run_count)]*1.
    run_accuracy = run_correct/run_count
    
    for r in range(len(run_count)):
         rlist = subinfo + [int(r),run_correct[r],run_count[r],run_accuracy[r]]
         summary_csvlist.append(rlist)
    
    
    # write to csv
    list2csv(data_csvlist,fname_out)
    print fname_out + ' saved.'

list2csv(summary_csvlist, fname_out_summary)
print fname_out_summary + ' saved. DONE.'
