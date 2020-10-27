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


import os, sys
sys.path.append(os.getcwd() + '/networkx')
import networkx as nx
sys.path.append(os.getcwd())
from psychopy_util import *
import random
import itertools
import ast
sys.path.append(os.getcwd() + '/../analyze')
from data_conversion_util import *
from config import *

def check_response(response):
    # kill command
    if response:
        if response[0] == QUIT_KEY:
            infoLogger.logger.info('WARNING: ' + QUIT_KEY + ' pressed. Exiting...')
            json2csv(json_file = DATA_FOLDER + filename + '.txt', csv_filename = DATA_FOLDER + filename + '.csv')
            infoLogger.logger.info('Data file converted to csv file')
            core.quit()


def show_time_limit_prompt(stim, response_keys=RESPONSE_KEYS):
    limit_rect_stim = visual.Rect(presenter.window, opacity=.5, width=5, height=0.2, lineWidth=0, fillColor=(-1,-1,-1))
    limit_text_stim = visual.TextStim(presenter.window, TRIAL_LIMIT_PROMPT, pos=(0,0), height=.15, wrapWidth=5, color=COLOR_WRONG)
    all_stim = stim + [limit_rect_stim, limit_text_stim]
    resp = presenter.draw_stimuli_for_response(all_stim, response_keys=response_keys)
    return resp

def trial_time_control(stim, response_keys=RESPONSE_KEYS):
    resp = presenter.draw_stimuli_for_response(stim, response_keys=response_keys, max_wait=MAX_TRIAL_TIME)
    if resp is None:
        resp = show_time_limit_prompt(stim, response_keys=response_keys)
        resp = list(resp)
        resp[1] = resp[1] + MAX_TRIAL_TIME
    return resp

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
    random.shuffle(nodes)
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
                                      TRAIN_TEXT.format(*TRAIN_TEXT_FILLINGS_POS[icond]),
                                      pos=(-0.6, 0.6),
                                      wrapWidth=0.5)
    connected_nodes = network.neighbors(node_index)
    nodes_stims = get_node_stims(connected_nodes, connected=True)
    stims = [bg] + nodes_stims + [images[node_index], labels[node_index], cont_stim, train_text_stim]
    response1 = trial_time_control(stims, response_keys=['space']) # show it
    check_response(response1)
    # unconnected nodes
    train_text_stim = visual.TextStim(presenter.window,
                                      TRAIN_TEXT.format(*TRAIN_TEXT_FILLINGS_NEG[icond]),
                                      pos=(-0.6, 0.6),
                                      wrapWidth=0.5)
    unconnected_nodes = [node for node in network.nodes()
                         if (node not in connected_nodes and node != node_index)]
    nodes_stims = get_node_stims(unconnected_nodes)
    stims = nodes_stims + [images[node_index], labels[node_index], cont_stim, train_text_stim]
    response2 = trial_time_control(stims, response_keys=['space']) # show it
    check_response(response2)
    #response2 = presenter.draw_stimuli_for_response(stims, ['space'])  # show it
    return {
        'rt_connected': response1[1],
        'rt_unconnected': response2[1],
        'node1' : node_index,
        'image1': images[node_index]._imName,
        'label1': labels_txt[node_index],
        'node2_connected': connected_nodes,
        'image2_connected': [images[i]._imName for i in connected_nodes],
        'label2_connected': [labels_txt[i] for i in connected_nodes],
        'node2_unconnected': unconnected_nodes,
        'image2_unconnected': [images[i]._imName for i in unconnected_nodes],
        'label2_unconnected': [labels_txt[i] for i in unconnected_nodes]
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
    response = trial_time_control(stims, response_keys=RESPONSE_KEYS) # show it
    check_response(response)
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
    x = trial_time_control(all_stim, response_keys=['space', QUIT_KEY])
    check_response(x)

    return {'node1': rand_i,
            'node2': rand_j,
            'image1': images[rand_i]._imName,
            'image2': images[rand_j]._imName,
            'label1': labels_txt[rand_i],
            'label2': labels_txt[rand_j],
            'connected': network.has_edge(rand_i, rand_j),
            'response': response[0],
            'rt': response[1],
            'correct': correct,
            'points': 'n/a' if total_points == sys.maxint else total_points}

def get_imgs_labels(sid, sectid):
    imgs = presenter.load_all_images(IMG_FOLDER, '.png')

    # read in mapping
    with open(IMG_MAPPINGS, 'r') as file:
        mappings = file.read().replace('\n', '')
    # remove "var subject_imgs = " string from beginning
    mappings = mappings.split(' = ')[1]
    # remove ';' from end
    mappings = mappings.split(';')[0]
    # convert string to dictionary and select subject's key and section
    mapping = ast.literal_eval(mappings)[sid][sectid+1]
    img_sect = []
    labels_sect = []
    for i in range(len(mapping)):
        img_name = os.path.join(IMG_FOLDER, os.path.basename(mapping[i][0]))
        label = mapping[i][1]
        for img in imgs:
            if img_name == img._imName:
                img_sect += [img]
                labels_sect += [label]
                break
    return {'images':img_sect,
            'labels':labels_sect
            }

def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # check age
    try:
        if int(items['Age']) < 18 and items['Mode'] != 'Test':
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
    icond = CONDITIONS[sid % len(CONDITIONS)]
    random.seed(sid)
    #random.shuffle(NETWORKS)
    sectid = int(sinfo['Section']) - 1
    sinfo['Condition'] = CONDITION_NAMES[icond]
    net_ind = (int(((sid % 4) == 3)) + sectid) % 2
    network_name = NETWORKS[net_ind] # select network
    sinfo['Structure'] = network_name
    FEEDBACK_FRIEND = FEEDBACK_FRIEND_TEXTS[icond]
    FEEDBACK_FOE = FEEDBACK_FOE_TEXTS[icond]
    # test mode
    mode_str = sinfo['Mode']
    test_bool = mode_str == 'Test'

    # create log files
    # name subject's data and log files with sid
    if test_bool:
        filename = FILENAME_PREFIX + mode_str+'%03d_sect-%01d' % (sid, sectid + 1)
    else:
        filename = FILENAME_PREFIX + '%03d_sect-%01d' % (sid, sectid + 1)
    infoLogger = DataLogger(LOG_FOLDER, filename + '.log', log_name='info_logger', logging_info=True, overwrite_file=(test_bool))
    dataLogger = DataLogger(DATA_FOLDER, filename + '.txt', log_name='data_logger', overwrite_file=(test_bool))
    # save info from the dialog box
    dataLogger.write_json({
        k: str(sinfo[k]) for k in sinfo.keys()
    })
    # create window
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger', background_color = BG_COLOR)

    # construct network
    network = nx.Graph()
    edges = EDGES[network_name]
    network.add_edges_from(edges)
    dataLogger.write_json(edges)
    num_nodes = network.number_of_nodes()

    # get subject's network, images, and labels for this section
    # load images
    il_dict = get_imgs_labels(sid, sectid)
    images = il_dict['images']
    labels_txt = il_dict['labels']
    train_img_size = presenter.pixel2norm(TRAIN_IMG_SIDE_LENGTH)
    dataLogger.write_json({i: (stim._imName, labels_txt[i]) for i, stim in enumerate(images)})
    labels = [visual.TextStim(presenter.window, text=label) for label in labels_txt]

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
    rect = visual.Rect(presenter.window, width=0.2, height=0.1, lineWidth=0, fillColor=BG_COLOR)
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
        fillings = INSTR_0_FILLINGS[i][icond]
        presenter.show_instructions(instr.format(*fillings))
    num_trials_train = min(num_nodes, MAX_NUM_TRIALS_PER_HALF_ROUND)
    num_trials_test = min(len(test_orders[0]), MAX_NUM_TRIALS_PER_HALF_ROUND)
    for r in range(NUM_ROUNDS):
        # training
        random.shuffle(train_order)
        round_txt = 'Round %d/%d\n\n' % (r + 1, NUM_ROUNDS)
        presenter.show_instructions(round_txt + INSTR_TRAIN.format(*INSTR_TRAIN_FILLINGS[icond]))
        for img in images:
            img.size = train_img_size
        for t in range(num_trials_train):
            node_index = train_order[t]
            rts = show_training_trial(node_index)
            # separate and remove connected and unconnected components
            rts_keys = rts.keys()
            rts_connected = {'connected': True}
            rts_unconnected = {'connected': False}
            for k in rts_keys:
                if '_connected' in k:
                    new_key = k.split('_')[0]
                    rts_connected[new_key] = rts.pop(k)
                elif '_unconnected' in k:
                    new_key = k.split('_')[0]
                    rts_unconnected[new_key] = rts.pop(k)
            # set elements for both connected and unconnected trials
            data = rts
            data['run_index'] = r
            data['trial_type'] = 'train'
            data['trial_index'] = t
            # save connected trial
            data.update(rts_connected)
            print(data)
            dataLogger.write_json(data)
            # save unconnected trial
            data.update(rts_unconnected)
            dataLogger.write_json(data)

        # test
        random.shuffle(test_orders[r % 2])
        presenter.show_instructions(INSTR_TEST.format(*INSTR_TEST_FILLINGS[icond]))
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
            data['run_index'] = r
            data['trial_type'] = 'test'
            data['trial_index'] = t
            dataLogger.write_json(data)
    presenter.show_instructions(INSTR_END, key_to_continue = QUIT_KEY, next_page_text='')
    # convert json to csv file
    json2csv(json_file = DATA_FOLDER + filename + '.txt', csv_filename = DATA_FOLDER + filename + '.csv')
    infoLogger.logger.info('Data file converted to csv file')
    infoLogger.logger.info('End of experiment')
