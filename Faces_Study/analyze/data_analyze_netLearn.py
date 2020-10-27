import os
from shutil import copy2 as cp
from data_conversion_util import *
from analysis_funcs_netLearn import *
import numpy as np
from igraph import *
old_err_state = np.seterr(divide='raise')
ignored_states = np.seterr(**old_err_state)



# choose which run to use from the learning task
learn_run = '1' #('0','1','all')
# analyze network learning task?
analyze_learn = False
# analyze network drawing task?
analyze_draw = True
# subjects to exclude
exclude_sub_list = [994, 995, 996, 997, 998, 30, 33, 44, 71, 118, 202, 229, 230]
# graph properties
n_nodes = 9
directed = False

# directories and filenames
proj_dir = '../'
learn_data_dir = proj_dir+'learning-task/data'
learn_fnames_in = get_subfiles(learn_data_dir,".csv")
learn_fname_out = learn_data_dir+'learn_accuracy.csv'
draw_data_dir = proj_dir+'drawing-task/'
draw_fname_in = draw_data_dir+'network-editor-v2-export.json'
draw_fname_out = draw_data_dir+'draw_accuracy.csv'
#data_dir = 'data/'
#fname_out_summary = data_dir+'learn_accuracy.csv'
#sub_files = get_subfiles(data_dir,".txt")

# read in network drawing data file (contains all subjects)
data_dict_draw = load_json(draw_fname_in)

subject_graphs_draw_AS = []
subject_graphs_draw_BS = []
subject_graphs_draw_AA = []
subject_graphs_draw_BA = []
subject_graphs_learn_AS = []
subject_graphs_learn_BS = []
subject_graphs_learn_AA = []
subject_graphs_learn_BA = []
sub_list_AS = []
sub_list_BS = []
sub_list_AA = []
sub_list_BA = []

count=0
for f in sub_files:
    count += 1
    subject_num = f.split('_')[0]
    section_num = f.split('_')[1].split('.')[0]
    # check if subject is to be excluded
    if subject_num in exclude_sub_list:
        print('Subject '+subject_num+ ' excluded.')
        continue
    # conversion filenames
    fname_in  = data_dir+subject_num+'_'+section_num+'.txt'
    fname_out = data_dir+subject_num+'_'+section_num+'.csv'

    # read in file
    data_dict = load_json(fname_in,multiple_obj=True)
    # extract subject information
    subinfo_hdr, subinfo = get_subinfo(data_dict)
    # header
    if count == 1:
        summary_csvlist = []
        summary_csvlist.append(subinfo_hdr+['run','accuracy','tp','fp','tn','fn'])

    # check if file needs to be converted
    if (not os.path.isfile(fname_out)) or overwrite:
        # extract and write subject data
        data_csvlist = subdata_convert_netLearn(data_dict)
        # write to csv
        list2csv(data_csvlist,fname_out)
        print fname_out + ' saved.'

    ## WRITE LEARN SUMMARY FILE
    # calculate run by run accuracy
    run_count, run_accuracy, run_rates = subdata_accuracy_netLearn(data_dict)
    # data
    for r in range(len(run_count)):
        rlist = subinfo + [int(r),run_accuracy[r], run_rates[0][r], run_rates[1][r], run_rates[2][r], run_rates[3][r]]
        summary_csvlist.append(rlist)

    ## SUBJECT'S GRAPH
    # extract subject's data for this section
    print 'analyzing subject ' + subject_num + ', section ' + section_num
    sub_data_draw = data_dict_draw['ucla'+subject_num][int(section_num)]
    sub_data_draw = sub_data_draw[sub_data_draw.keys()[0]]['data']
    sub_edges = []
    # go through each node's data
    for n in sub_data_draw:
        node = n['id']
        node = int(node)
        # if connections were drawn from this node...
        if 'connections' in n.keys():
            # get alters for this node
            alters = n['connections']
            if not directed:
                # if not a directed graph, keep only unique pairs
                # ignore alters that you have already been analyzed
                for alter in alters:
                    if alter > node:
                        sub_edges.append((node,alter))
    sub_g_draw = Graph(n=n_nodes,edges=sub_edges,directed=directed)
    sub_g_learn = get_graph_netLearn(data_dict, run_number=learn_run)
    if data_dict[0]['NetworkType']=='social':
        # social condition
        if len(data_dict[1]) == 15:
            # network A
            subject_graphs_draw_AS.append(sub_g_draw)
            subject_graphs_learn_AS.append(sub_g_learn)
            true_graph_A = Graph(edges=data_dict[1],directed=directed)
            sub_list_AS.append(subject_num)
        else:
            # network B
            subject_graphs_draw_BS.append(sub_g_draw)
            subject_graphs_learn_BS.append(sub_g_learn)
            true_graph_B = Graph(edges=data_dict[1],directed=directed)
            sub_list_BS.append(subject_num)
    else:
        # non-social condition
        if len(data_dict[1]) == 15:
            # network A
            subject_graphs_draw_AA.append(sub_g_draw)
            subject_graphs_learn_AA.append(sub_g_learn)
            true_graph_A = Graph(edges=data_dict[1],directed=directed)
            sub_list_AA.append(subject_num)
        else:
            # network B
            subject_graphs_draw_BA.append(sub_g_draw)
            subject_graphs_learn_BA.append(sub_g_learn)
            true_graph_B = Graph(edges=data_dict[1],directed=directed)
            sub_list_BA.append(subject_num)
labels = ['AA','BA','AS','BS']

# write out all subjects to one data file
AS_edges_out, AS_edges_out_long = analyze_local_graph(true_g = true_graph_A,
                                                      sub_list = sub_list_AS,
                                                      sub_graphs_draw = subject_graphs_draw_AS,
                                                      sub_graphs_learn = subject_graphs_learn_AS,
                                                      network = 'A',
                                                      condition = 'S')
BS_edges_out, BS_edges_out_long = analyze_local_graph(true_graph_B,
                                                      sub_list_BS,
                                                      subject_graphs_draw_BS,
                                                      subject_graphs_learn_BS,
                                                      'B','S')
AA_edges_out, AA_edges_out_long = analyze_local_graph(true_graph_A,
                                                      sub_list_AA,
                                                      subject_graphs_draw_AA,
                                                      subject_graphs_learn_AA,
                                                      'A','A')
BA_edges_out, BA_edges_out_long = analyze_local_graph(true_graph_B,
                                                      sub_list_BA,
                                                      subject_graphs_draw_BA,
                                                      subject_graphs_learn_BA,
                                                      'B','A')

#remove headers
del BS_edges_out[0]
del AA_edges_out[0]
del BA_edges_out[0]
del BS_edges_out_long[0]
del AA_edges_out_long[0]
del BA_edges_out_long[0]

edges_all_out = AS_edges_out+BS_edges_out+AA_edges_out+BA_edges_out
list2csv(edges_all_out,'data/edges_all.csv')
edges_all_out_long = AS_edges_out_long+BS_edges_out_long+AA_edges_out_long+BA_edges_out_long
list2csv(edges_all_out_long,'data/edges_all_long.csv')
print 'edges_all files saved.'

list2csv(summary_csvlist, fname_out_summary)
print fname_out_summary + ' saved. DONE.'
