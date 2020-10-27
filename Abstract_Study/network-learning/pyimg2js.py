#!/usr/bin/env python

# TODO temporary file; need to change according to netLearn.py

import os, sys
sys.path.append(os.getcwd() + '/networkx')

import networkx as nx
import random
import os
from config import IMG_FOLDER, EDGES, LABELS
from copy import deepcopy

NUM_SECTIONS = 2
NUM_NODES = 9  # 9 or 15
images = [filename for filename in sorted(os.listdir(IMG_FOLDER)) if filename.endswith('.png')]

with open('subject_imgs.js', 'w') as outfile:
    outfile.write('var subject_imgs = {')
    for sid in range(0, 501):
        outfile.write(str(sid) + ': {')
        for sectid in range(NUM_SECTIONS):
            images = sorted(images)
            edges = deepcopy(EDGES)
            labels = deepcopy(LABELS)
            network = nx.Graph()
            network.add_edges_from(edges[sectid][NUM_NODES])
            num_nodes = network.number_of_nodes()
            # randomize
            random.seed(sid)
            random.shuffle(images)
            sect_imgs = images[sectid * num_nodes : (sectid + 1) * num_nodes]
            random.shuffle(edges)
            sect_labels = labels[sectid * num_nodes : (sectid + 1) * num_nodes]
            random.shuffle(sect_labels)
            # get string
            sect_tuples = ["'" + img + "', '" + label + "'" for img, label in zip(sect_imgs, sect_labels)]
            outfile.write(str(sectid + 1) + ': [')
            outfile.write("[" + "], [".join(sect_tuples) + "]")  # ['img', 'label'], ['img', 'label'], ...
            outfile.write('], ')
        outfile.write('}, ')
    outfile.write('};\n')
