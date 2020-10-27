#!/usr/bin/env python

# TODO temporary file; need to change according to netLearn.py

import os, sys
sys.path.append(os.getcwd() + '/networkx')

import networkx as nx
import random
import os
from copy import deepcopy
from config import IMG_FOLDER, EDGES, NETWORKS, LABELS, IMG_PREFIXES1, IMG_PREFIXES8, IMG_MAPPINGS

def get_imgs(sectid):
    imgs = ['../' + IMG_FOLDER + f for f in sorted(os.listdir(IMG_FOLDER)) if f.endswith('.png')]
    random.shuffle(imgs)
    random.shuffle(IMG_PREFIXES8)
    random.shuffle(IMG_PREFIXES1)

    # select the sectid element of each array of images matching IMG_PREFIXES8 elements
    img_sect = []
    for pref in IMG_PREFIXES8:
        pi = []
        for img in imgs:
            if pref in img:
                # add actual image object
                pi += [img]
        # select one element of array of images
        print(pi)
        img_sect += [pi[sectid]]
    # add last element by finding all images that match one of the IMG_PREFIXES1 elements
    # select the last element and add to selected images
    pi = []
    for img in imgs:
        if IMG_PREFIXES1[sectid] in img:
            pi += [img]
    img_sect += [pi[-1]]

    # shuffle order a different number of times for each section
    for i in range(sectid):
        random.shuffle(img_sect)

    return img_sect


with open(IMG_MAPPINGS, 'w') as outfile:
    outfile.write('var subject_imgs = {')
    for sid in range(0, 1000):
        outfile.write(str(sid) + ': {')
        for sectid in range(len(EDGES)):
            edges = deepcopy(EDGES)
            labels = deepcopy(LABELS)
            network = nx.Graph()
            network.add_edges_from(edges[NETWORKS[sectid]])
            num_nodes = network.number_of_nodes()
            # randomize
            random.seed(sid)
            random.shuffle(NETWORKS)
            sect_imgs = get_imgs(sectid)
            random.shuffle(labels)
            sect_labels = labels[sectid * num_nodes:(sectid + 1) * num_nodes]
            random.shuffle(sect_labels)
            # get string
            sect_tuples = ["'" + img + "', '" + label + "'" for img, label in zip(sect_imgs, sect_labels)]
            outfile.write(str(sectid + 1) + ': [')
            outfile.write("[" + "], [".join(sect_tuples) + "]")  # ['img', 'label'], ['img', 'label'], ...
            outfile.write('], ')
        outfile.write('}, ')
    outfile.write('};\n')
