#!/usr/bin/env python
"""
Network Learning Experiment (run script in Psychopy)

Variables read from config.py
Functions read from psychopy_util.py
Paradigm (Winter 2017):
    2 conditions: social (even participants), non-social (odd participants)
    2 parts, each with distinct network (EDGES[0] and EDGES[1]):
        Iterates through all nodes, showing all connections and non-connections to each node
        Shows 2 nodes at a time, participant guesses if they are linked in the network
            Feedback given:
                correct/incorrect
                line connecting two images with or without an 'X'
                feedback text describing relationship 
"""

from config import *

import os, sys
sys.path.append(os.getcwd() + '/networkx')
import networkx as nx
from psychopy_util import *
import random
import itertools


def make_grid(num_elt, elt_interval, min_margin=0.0):
    """
    # TODO write docstring and put this in psychopy_util
    :param num_elt: (integer) number of elements
    :param elt_interval: (float) distance between elements
    :param min_margin: (float) distance to the edges of the screen
    :return: a list of float values
    """
    if num_elt == 0:
        return []
    if num_elt == 1:
        return [0.0]
    width = (num_elt - 1) * elt_interval
    if width > 2 - min_margin:
        positions = [float(pos) / 100
                     for pos in range(-100 + int(min_margin * 100), 101 - int(min_margin * 100),
                                      int((200 - min_margin * 200) / (num_elt - 1)))]
    else:
        positions = [float(pos) / 100
                     for pos in range(-int(width * 50), int(width * 50) + 2,
                                      int(elt_interval * 100))]
    return positions


def get_node_stims(nodes, connected=False):
    image_stims = [images[i] for i in nodes]
    label_stims = [labels[i] for i in nodes]
    x_values = make_grid(len(nodes), elt_interval=0.5, min_margin=MIN_MARGIN)
    lines = []
    two_rows = len(nodes) > 6
    for i in range(len(nodes)):
        if two_rows:
            image_stims[i].pos = (x_values[i], TRAIN_BOTTOM_IMG_Y[1][i % 2])
            label_stims[i].pos = (x_values[i], TRAIN_BOTTOM_LABEL_Y[1][i % 2])
        else:
            image_stims[i].pos = (x_values[i], TRAIN_BOTTOM_IMG_Y[0])
            label_stims[i].pos = (x_values[i], TRAIN_BOTTOM_LABEL_Y[0])
        if connected:
            lines.append(visual.Line(win=presenter.window,
                                     lineWidth=50,
                                     lineColor=color_friend,
                                     start=TRAIN_TOP_IMG_POS,
                                     end=image_stims[i].pos))
    if connected:
        return lines + image_stims + label_stims
    return image_stims + label_stims


def show_training_trial(node_index):
    # constant stimuli
    images[node_index].pos = TRAIN_TOP_IMG_POS
    labels[node_index].pos = TRAIN_TOP_LABEL_POS
    cont_stim = visual.TextStim(presenter.window, CONT_TEXT, pos=(0.6, 0.6), height=0.07)
    # connected nodes
    train_text_stim = visual.TextStim(presenter.window,
                                      TRAIN_TEXT.format(*TRAIN_TEXT_FILLINGS_POS[sid % 2]),
                                      pos=(-0.6, 0.6),
                                      wrapWidth=0.5)
    connected_nodes = network.neighbors(node_index)
    nodes_stims = get_node_stims(connected_nodes, connected=True)
    stims = [bg] + nodes_stims + [images[node_index], labels[node_index], cont_stim, train_text_stim]
    response1 = presenter.draw_stimuli_for_response(stims, ['space'])  # show it
    # unconnected nodes
    train_text_stim = visual.TextStim(presenter.window,
                                      TRAIN_TEXT.format(*TRAIN_TEXT_FILLINGS_NEG[sid % 2]),
                                      pos=(-0.6, 0.6),
                                      wrapWidth=0.5)
    unconnected_nodes = [node for node in network.nodes()
                         if (node not in connected_nodes and node != node_index)]
    nodes_stims = get_node_stims(unconnected_nodes)
    stims = nodes_stims + [images[node_index], labels[node_index], cont_stim, train_text_stim]
    response2 = presenter.draw_stimuli_for_response(stims, ['space'])  # show it
    return {
        'rt_connected': response1[1],
        'rt_unconnected': response2[1]
    }


def show_test_trial(order):
    global total_points
    # image positions
    rand_i = order[0]
    rand_j = order[1]
    images[rand_i].pos = presenter.LEFT_CENTRAL_POS
    images[rand_j].pos = presenter.RIGHT_CENTRAL_POS
    labels[rand_i].pos = (-0.5, -0.35)
    labels[rand_j].pos = (0.5, -0.35)
    # fixation
    presenter.show_fixation(FIXATION_TIME)
    # get response
    stims = [images[rand_i], images[rand_j], labels[rand_i], labels[rand_j]]
    if total_points != sys.maxint:
        point_stim = visual.TextStim(presenter.window, POINTS_TEXT % total_points, pos=POINTS_POS)
        stims.append(point_stim)
    response = presenter.draw_stimuli_for_response(stims, response_keys=RESPONSE_KEYS)
    correct = (response[0] == RESPONSE_KEYS[0] and not network.has_edge(rand_i, rand_j)) or \
              (response[0] == RESPONSE_KEYS[1] and network.has_edge(rand_i, rand_j))
    # correct/incorrect feedback
    feedback = FEEDBACK_RIGHT if correct else FEEDBACK_WRONG
    feedback_color = COLOR_RIGHT if correct else COLOR_WRONG
    feedback_stim = visual.TextStim(presenter.window, text=feedback, color=feedback_color, pos=(0, .5))
    # friend/foe feedback
    friendorfoe = FEEDBACK_FRIEND if network.has_edge(rand_i, rand_j) else FEEDBACK_FOE
    friendorfoe_color = color_friend if network.has_edge(rand_i, rand_j) else color_foe
    friendorfoe_stim = visual.TextStim(presenter.window, text=friendorfoe, color=friendorfoe_color, pos=(0, -.5))

    # display feedback screen
    stims.append(feedback_stim)
    if total_points != sys.maxint:
        point_change = 1 if correct else -3
        stims.append(visual.TextStim(presenter.window,
                                     '%+d' % point_change,
                                     color=feedback_color,
                                     pos=POINTS_CHANGE_POS))
        total_points += point_change
        new_point_stim = visual.TextStim(presenter.window, POINTS_TEXT % total_points, pos=POINTS_POS)
    presenter.draw_stimuli_for_duration(stims, duration=FEEDBACK_CORRECT_TIME)
    # more feedback
    if network.has_edge(rand_i, rand_j):
        line.lineColor = color_friend
        all_stim = [bg, line] + stims + [friendorfoe_stim]
    else:
        line.lineColor = COLOR_CONNECTION_AUXILIARY
        all_stim = [line, rect, X1, X2] + stims + [friendorfoe_stim]
    if total_points != sys.maxint:
        all_stim.remove(point_stim)
        all_stim.append(new_point_stim)
    presenter.draw_stimuli_for_duration(all_stim, duration=(FEEDBACK_TIME - FEEDBACK_CORRECT_TIME))
    all_stim.append(visual.TextStim(presenter.window, CONT_TEXT, pos=(0.0, -0.8)))
    presenter.draw_stimuli_for_response(all_stim, response_keys=['space'])

    return {'images': (rand_i, rand_j),
            'connected': network.has_edge(rand_i, rand_j),
            'response': response,
            'correct': correct,
            'points': 'NA' if total_points == sys.maxint else total_points}


def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # check age
    try:
        if int(items['Age']) <= 0:
            raise ValueError
    except ValueError:
        return False, 'Age must be a positive integer'
    # everything is okay
    return True, ''


if __name__ == '__main__':
    # subject ID dialog
    sinfo = dialog_info
    show_form_dialog(sinfo, validation, order=dialog_order)
    sid = int(sinfo['ID'])
    random.seed(sid)
    sectid = int(sinfo['Section']) - 1
    sinfo['NetworkType'] = 'social' if sid % 2 == 0 else 'airport'
    FEEDBACK_FRIEND = FEEDBACK_FRIEND_TEXTS[sid % 2]
    FEEDBACK_FOE = FEEDBACK_FOE_TEXTS[sid % 2]

    # create log files
    filename = str(sid) + '_' + str(sectid + 1)
    infoLogger = DataLogger(LOG_FOLDER, filename + '.log', log_name='info_logger', logging_info=True)
    dataLogger = DataLogger(DATA_FOLDER, filename + '.txt', log_name='data_logger')
    # save info from the dialog box
    dataLogger.write_json({
        k: str(sinfo[k]) for k in sinfo.keys()
    })
    # create window
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger')
    # load images
    images = presenter.load_all_images(IMG_FOLDER, '.png')
    random.shuffle(images)
    random.shuffle(EDGES)
    train_img_size = presenter.pixel2norm(TRAIN_IMG_SIDE_LENGTH)
    # construct network
    network = nx.Graph()
    network.add_edges_from(EDGES[sectid][NUM_NODES])
    dataLogger.write_json(EDGES[sectid][NUM_NODES])
    num_nodes = network.number_of_nodes()
    if num_nodes <= .5 * len(images):
        images = images[sectid * num_nodes:(sectid+1) * num_nodes]
    else:
        raise ValueError('Number of images (%d) less than number of nodes (%d)' % (len(images), num_nodes))
    # labels
    labels = LABELS[sectid * num_nodes:(sectid+1) * num_nodes]
    random.shuffle(labels)
    dataLogger.write_json({i: (stim._imName, labels[i]) for i, stim in enumerate(images)})
    labels = [visual.TextStim(presenter.window, text=label) for label in labels]
    # randomize colors
    random.shuffle(COLORS_CONNECTION)
    color_friend, color_foe = COLORS_CONNECTION
    # set order of stimuli
    train_order = list(range(num_nodes))
    test_orders = [subset for subset in itertools.combinations(range(num_nodes), 2)]
    # order[1] is same as order[0] except images are on different sides
    test_orders = [test_orders, [(y, x) for x, y in test_orders]]
    # feedback visual
    line = visual.Line(
        win=presenter.window,
        lineWidth=5,
        start=presenter.LEFT_CENTRAL_POS,
        end=presenter.RIGHT_CENTRAL_POS
    )
    rect = visual.Rect(presenter.window, width=0.2, height=0.1, lineWidth=0, fillColor=(0, 0, 0))
    X1 = visual.Line(
        win=presenter.window,
        lineColor=color_foe,
        lineWidth=50,
        start=(-1 * X_SIZE, -1.5 * X_SIZE),
        end=(X_SIZE, 1.5 * X_SIZE)
    )
    X2 = visual.Line(
        win=presenter.window,
        lineColor=color_foe,
        lineWidth=50,
        start=(-1 * X_SIZE, 1.5 * X_SIZE),
        end=(X_SIZE, -1.5 * X_SIZE)
    )
    # background for connected nodes
    bg = visual.Rect(presenter.window, width=2.1, height=2.1, lineWidth=0, fillColor=FRIEND_BG_COLOR)

    # experiment starts
    total_points = sys.maxint
    for i, instr in enumerate(INSTR_0):
        fillings = INSTR_0_FILLINGS[i][sid % 2]
        presenter.show_instructions(instr.format(*fillings))
    num_trials_train = min(num_nodes, MAX_NUM_TRIALS_PER_HALF_ROUND)
    num_trials_test = min(len(test_orders[0]), MAX_NUM_TRIALS_PER_HALF_ROUND)
    for r in range(NUM_ROUNDS):
        # training
        random.shuffle(train_order)
        round_txt = 'Round %d/%d\n\n' % (r + 1, NUM_ROUNDS)
        presenter.show_instructions(round_txt + INSTR_TRAIN.format(*INSTR_TRAIN_FILLINGS[sid % 2]))
        for img in images:
            img.size = train_img_size
        for t in range(num_trials_train):
            node_index = train_order[t]
            data = show_training_trial(node_index)
            data['image'] = node_index
            data['trial_index'] = '%d.train.%d' % (r, t)
            dataLogger.write_json(data)
        # test
        random.shuffle(test_orders[r % 2])
        presenter.show_instructions(INSTR_TEST.format(*INSTR_TEST_FILLINGS[sid % 2]))
        if r == ROUND_SHOWING_POINTS:
            total_points = 0
            points_stim = visual.TextStim(presenter.window, POINTS_TEXT % total_points, pos=POINTS_POS)
            presenter.show_instructions(INSTR_POINTS, other_stim=(points_stim,))
        elif r < ROUND_SHOWING_POINTS:
            presenter.show_instructions(INSTR_PRACTICE)
        if r >= ROUND_SHOWING_POINTS:
            total_points = 0
        for img in images:
            img.size = None
        for t in range(num_trials_test):
            data = show_test_trial(test_orders[r % 2][t])
            data['trial_index'] = '%d.test.%d' % (r, t)
            dataLogger.write_json(data)
    presenter.show_instructions(INSTR_END)
