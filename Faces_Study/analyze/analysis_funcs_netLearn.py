#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 15:52:06 2018

@author: miriam
"""

import os
from shutil import copy2 as cp
from data_conversion_util import *
import numpy as np
from igraph import *
old_err_state = np.seterr(divide='raise')
ignored_states = np.seterr(**old_err_state)


def copy_data_files(orig_data_dir,new_data_dir):
    # copy data files from orig_data_dir to new_data_dir
    for file in os.listdir(orig_data_dir):
        if file.endswith(".txt"):
            orig_file_path = os.path.join(orig_data_dir, file)
            new_file_path = os.path.join(new_data_dir, file)
            if not os.path.isfile(new_file_path):
                print 'copying file '+ orig_file_path + ' to ' + new_file_path
                cp(orig_file_path,new_data_dir)

def get_subfiles(data_dir,file_ext):
    sub_files=[]
    for file in os.listdir(data_dir):
        if file.endswith(file_ext):
            sub_files.append(file)
    return sorted(sub_files)

def get_subinfo(data_dict):
    # determine which of the two networks was seen
    if len(data_dict[1]) == 15:
    	structure='A'
    elif len(data_dict[1]) == 8:
    	structure='B'
        
    # subinfo header
    subinfo_hdr = ['subID','section','structure','condition']
    # extract subject info (same for every trial per participant)
    subinfo_data = [data_dict[0]['ID'], data_dict[0]['Section'], structure, 
                    data_dict[0]['NetworkType']]
    
    return subinfo_hdr, subinfo_data
    
def subdata_convert_netLearn(data_dict):
    # get subinfo
    subinfo_hdr, subinfo = get_subinfo(data_dict)
    
    # initialize 2D list
    data_csvlist = []
    # header for subject info
    data_csvlist.append(subinfo_hdr + 
                        ['run','block','trial','connected','image1','image2',
                         'initial1','initial2','nodeIndex1','nodeIndex2',
                         'response','rt','correct'])
    ## build csv file row by row
    # go through each row in data file
    for i in range(3,len(data_dict)):
        # r = all data from current row
        r=data_dict[i]
        # tindex = array(row,block,trial)
        tindex=r['trial_index'].split('.')
        # if training trial
        if 'train' in r['trial_index']:
             block = 'train'
             run = tindex[0]
             # t1 = trial showing connected alters
             t1 = int(tindex[-1])*2
             # t2 = trial showing unconnected alters
             t2 = int(tindex[-1])*2+1
             # image ID
             image1 = data_dict[2][str(r['image'])][0]
             initial1 = data_dict[2][str(r['image'])][1]
             image2 = 'NA'
             initial2 = 'NA'
             nodeIndex1 = r['image']
             nodeIndex2 = 'NA'
             response = 'NA'
             rt = r['rt_connected']
             correct = 'NA'
             # rlist = connected trial data
             rlist = subinfo + [run,block,t1,True,image1,image2,initial1,initial2,
                                nodeIndex1,nodeIndex2,response,rt,correct]
             # add connected trial data to write out
             data_csvlist.append(rlist)
             rt = r['rt_unconnected']
             # rlist = uncconected trial data
             rlist = subinfo + [run,block,t2,False,image1,image2,initial1,initial2,
                                nodeIndex1,nodeIndex2,response,rt,correct]
             # add unconnected trial data to write out
             data_csvlist.append(rlist)
        # if test trial
        elif 'test' in r['trial_index']:
            block = 'test'
            # person 1
            nodeIndex1 = r['images'][0]
            # person 2
            nodeIndex2 = r['images'][1]
            # person 1's image
            image1 = data_dict[2][str(nodeIndex1)][0]
            initial1 = data_dict[2][str(nodeIndex1)][1]
            # person 2's image
            image2 = data_dict[2][str(nodeIndex2)][0]
            initial2 = data_dict[2][str(nodeIndex2)][1]
            # get participant's response
            if r['response'][0] == 'left':
                response = 'N'
            elif r['response'][0] == 'right':
                response = 'Y'
            # rlist = trial data
            rlist = subinfo + [tindex[0], 'test', t1, r['connected'], image1, 
                               image2, initial1, initial2, nodeIndex1, 
                               nodeIndex2, response, r['response'][1], r['correct']]
            # add trial data to write out
            data_csvlist.append(rlist)
    return data_csvlist

def subdata_accuracy_netLearn(data_dict):
    ## ACCURACY
    # initialize run count (for up to 10 runs)
    run_count = np.array([0])
    run_pos = np.array([0])
    run_neg = np.array([0])
    # initialize run accuracy count 
    run_correct = np.array([0])
    # initialize run rate counts: tp, fp, tn, fn
    run_rates = np.array([[0],[0],[0],[0]])
    
    # go through each row in data file
    for i in range(3,len(data_dict)):
        # r = all data from current row
        r = data_dict[i]
        # tindex = [row, block, trial]
        tindex=r['trial_index'].split('.')
        if 'test' in r['trial_index']:
            # current trial's run number
            run_num = int(tindex[0])
            # if new run, add element to run arrays
            if run_num >= len(run_count):
                run_count = np.append(run_count,[0])
                run_pos = np.append(run_pos,[0])
                run_neg = np.append(run_neg,[0])
                run_correct = np.append(run_correct,[0])
                run_rates = [np.append(run_rates[0],[0]),
                             np.append(run_rates[1],[0]),
                             np.append(run_rates[2],[0]),
                             np.append(run_rates[3],[0])]
            # add 1 to run counter
            run_count[run_num] += 1
            # add 1 to counter if trial is correct
            if r['correct']:
                # true
                run_correct[run_num] += 1
                if r['connected']:
                    # true positive
                    run_rates[0][run_num] += 1
                    run_pos[run_num] += 1
                else:
                    # true negative
                    run_rates[2][run_num] += 1
                    run_neg[run_num] += 1
            elif r['connected']:
                # false negative
                run_rates[3][run_num] += 1
                run_pos[run_num] += 1
            else:
                # false positive
                run_rates[1][run_num] += 1
                run_neg[run_num] += 1
                    
    # calculate accuracy
    run_accuracy = np.divide(np.multiply(run_correct,1.),run_count)
    run_rates = np.divide(np.multiply(run_rates,1.),[run_pos,run_neg,run_neg,run_pos])
    
    return run_count, run_accuracy, run_rates



def get_graph_netLearn(data_dict, run_number='1'):
    # edge list
    edgelist = []
    n_nodes = 0
    # go through each row in data file
    for i in range(3,len(data_dict)):
        # r = all data from current row
        r = data_dict[i]
        tindex=r['trial_index'].split('.')
        if 'test' in r['trial_index']:
            if str(run_number) == tindex[0] or run_number == 'all':
                # person 1
                node1 = r['images'][0]
                # person 2
                node2 = r['images'][1]
                if 'right' in r['response']:
                    # answered yes
                    edgelist.append((node1,node2))
                n_nodes = max(node1+1,node2+1,n_nodes)
    
    g = Graph(n=n_nodes, edges=edgelist, directed=False)
    return g

    
def analyze_local_graph(true_g, sub_list, sub_graphs_draw, sub_graphs_learn, network, condition):
    out = []
    out_long = []
    all_sub_graphs = [sub_graphs_draw, sub_graphs_learn]
    all_sub_graphs_labels = ['draw','learn']
    # summary header
    hdr = ['node1','node2','network','condition','in_network','task','prop_reported']
    out.append(hdr)
    
    # add header to output by subject
    #out_long.append(['subID']+hdr)
    out_long.append(['subID','node1','node2','network','condition','in_network','task','sub_reported'])
    
    vertices = range(len(true_g.vs))
    edges = true_g.get_edgelist()
    all_combs = []
    true_edges = []
    # go through all possible edges (i.e. node pairing)
    for i in range(true_g.vcount() - 1):
        for j in range(i+1,true_g.vcount()):
            # edge
            all_combs.append((i,j))
            # in network?
            e_in = true_g[i,j]
            true_edges.append(e_in)
            
            all_task_sub = []
            taskindex = 0
            for task_graphs in all_sub_graphs:
                # initialize count for rates: true positive (tp), false positive (fp),
                #     true negative (tn), and false negative (fn)
                
                task_label = all_sub_graphs_labels[taskindex]
                
                edge_info = [i, j, network, condition, e_in, task_label]
                
                subindex=0
                count=0
                for s in task_graphs:
                    # move on to next subject if out of range for the subject
                    if i >= s.vcount() or j >= s.vcount:
                        continue
                    
                    sub_num = sub_list[subindex]
                    
                    # in subject's graph?
                    s_in = s[i,j]
                    count = count + s_in

                    # calculate rates for this subject: tp, fp, tn, fn
                    #    edge in subject graph * edge in true graph
                    #    = 1 if both true, 0 if one or neither true
                    # add row to out_long
                    out_long.append([sub_num]+ edge_info +[s_in])
                    subindex += 1
                taskindex += 1
                # proportion of subjects who perceived this edge in this task
                sprop_in = count * 1. / len(task_graphs)
                row_out = edge_info + [sprop_in]
                    
                # calculate mean rates for this task
                
                # add to output
                # add this task to info 
                
            # build out_long rows for this edge including all subjects
            #row_out_long=[x+y+z for x,y,z in zip(sub_list,edge_info_rep,all_tasks)]
            
            out.append(row_out)
            #out_long = out_long + row_out_long
            
    return out,out_long
    