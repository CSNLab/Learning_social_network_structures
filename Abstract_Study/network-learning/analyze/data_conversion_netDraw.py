from data_conversion_util import *

NUM_NODES = 9

fname_in = 'data/network-editor-export.json'
fname_out_data = 'data/network-editor_data.csv'
fname_out_summary = 'data/network-editor_accuracy_data.csv'

# read in file
data_dict = load_json(fname_in)

subIDs = data_dict.keys()

out_list = []
out_list.append(['subID','Node1','Node2','TrueEdge','SubEdge','TruePos','FalsePos','TrueNeg','FalseNeg'])

out_summary_list = []
out_summary_list.append(['subID','NetworkType','tp_rate','fp_rate','tn_rate','fn_rate'])

# cycle through dictionary (1 per subject)
for s in subIDs:
	# extract subject number
	subID = s.split('ucla')[1]

	# determine which of the two networks was seen
	datafile_learn = load_json('data/'+subID+'_1.txt',multiple_obj=True)
	networkType = datafile_learn[0]['NetworkType']

	true_edges = datafile_learn[1]
	total_true_edges = len(true_edges)

	all_combs = []
	for i in range(8):
		for j in range(i+1,9):
			all_combs.append([i,j])
	neg_edges = [i for i in all_combs if i not in true_edges]
	total_neg_edges = len(neg_edges)


	sub_data = data_dict[s][1]
	# get first entry
	sub_data = sub_data[sub_data.keys()[0]]['data']
	sub_edges = []

	for n in sub_data:
		node = n['id']
		node = int(node)
		if 'connections' in n.keys():
			alters = n['connections']
			for alter in alters:
				if alter > node:
					sub_edges.append([node,alter])

	#all_edges = []
	counts = [0,0,0,0]
	for e in all_combs:
		true_e = e in true_edges
		sub_e = e in sub_edges
		false_e = e in neg_edges
		tp = int(true_e&sub_e)
		fp = int(false_e&sub_e)
		tn = int(false_e & (not sub_e))
		fn = int(true_e&(not sub_e))
		tfpn = [tp,fp,tn,fn]
		#print(e,tfpn)
		counts = [x+y for x,y in zip(counts,tfpn)]
		r = [subID]+e+[true_e]+[sub_e]+tfpn
		out_list.append(r)

	tp_rate = float(counts[0])/total_true_edges
	fp_rate = float(counts[1])/total_neg_edges
	tn_rate = float(counts[2])/total_neg_edges
	fn_rate = float(counts[3])/total_true_edges
	out_summary_list.append([subID,networkType,tp_rate,fp_rate,tn_rate,fn_rate])



# write to csv
list2csv(out_list,fname_out_data)
list2csv(out_summary_list,fname_out_summary)

print 'Saved files: ' + fname_out_data + ' and ' + fname_out_summary