# Numbers
MAX_NUM_TRIALS_PER_HALF_ROUND = 999  # change to 999 (or any big number) if running all combinations
NUM_ROUNDS = 2
ROUND_SHOWING_POINTS = 0  # points earned are shown starting from this round index
NUM_NODES = 9  # 9 or 15

# Dialog
dialog_info = {'ID': '', 'Age': '', 'Section': ['1', '2'], 'Mode': ['Exp', 'Test']}
dialog_order=['ID', 'Age', 'Section', 'Mode']

# Paths
IMG_FOLDER = 'img_circ/'
DATA_FOLDER = 'data/'
LOG_FOLDER = 'log/'

# Times
FIXATION_TIME = 0.25
FEEDBACK_CORRECT_TIME = .25
FEEDBACK_TIME = 2

# Feedback visual
X_SIZE = .1

# Keys
RESPONSE_KEYS = ('left', 'right')  # (no, yes)

# Colors
FRIEND_BG_COLOR = '#81adc1'  # grey-ish blue
COLOR_RIGHT = '#53fc53'  # light green
COLOR_WRONG = '#ff0000'  # red
COLORS_CONNECTION = ['blue', 'yellow']
COLOR_CONNECTION_AUXILIARY = '#000000'  # black

# Positions and distances
TRAIN_TOP_IMG_POS = (0, 0.7)
TRAIN_TOP_LABEL_POS = (0, 0.4)
TRAIN_BOTTOM_IMG_Y = (-0.5, (-0.05, -0.63))       # (one_row, (top_row_in_two_rows, bottom_row_in_two_rows))
TRAIN_BOTTOM_LABEL_Y = (-0.8, (-0.35, -0.93))
TRAIN_IMG_SIDE_LENGTH = 250  # in pixels
MIN_MARGIN = 0.15
POINTS_POS = (0.75, 0.9)
POINTS_CHANGE_POS = (0.9, 0.8)

# Strings
LABELS = ['EPJ', 'EAG', 'MBF', 'RLA', 'SBJ', 'WSG', 'TDH', 'DWM', 'MLH',
          'LBK', 'KJT', 'LCF', 'ENM', 'DBG', 'RMJ', 'NFD', 'DKP', 'ACW',
          'HGP', 'NKS', 'RNP', 'JGC', 'GFT', 'EBH', 'NWB', 'EKF', 'AFH', 'LWP']
INSTR_0 = ['Welcome to the experiment!',
           'In this task, you will learn a network of {}. Some {}, and some are not.',              # 1
           'There will be {} rounds, during which you will have the opportunity to earn points.'    # 2
           '\n\nIn each round, you will first see each {}, {}, and {} not.',                        # 2
           'After seeing the entire network of {}, you will be tested on that information -- '      # 3
           'you will see every possible pair of {}, and answer whether or not they are {}. '        # 3
           'You will earn points by answering correctly, '                                          # 3
           'and you will lose points by answering incorrectly.',                                    # 3
           'Each {} is represented by {} and an abstract image that has nothing to do with {}, '    # 4
           'so please only pay attention to the {}.',                                               # 4
           'You will see your performance on this task later, so pay close attention '              # 5
           'to which {}!',                                                                          # 5
           'End of instructions. Please let the experimenter know you have finished the '           # 6
           'instructions before continuing.']                                                       # 6
INSTR_0_FILLINGS = \
    [[(), ()],
     [('people', 'people are friends'),                                                             # 1
      ('airports', 'airports are connected by a direct flight')],                                   # 1
     [(str(NUM_ROUNDS), 'person',                             # 2
       'everyone who is friends with this person', 'everyone who is'),                              # 2
      (str(NUM_ROUNDS), 'airport',                            # 2
       'which airports are connected to this airport by a direct flight', 'which ones are')],       # 2
     [('people', 'people', 'friends'), ('airports', 'airports', 'connected by a direct flight')],   # 3
     [('person', 'their initials', 'who they are', 'relationship between people'),                  # 4
      ('airport', 'a randomly generated airport code', 'where it is located',                       # 4
       'connections between airports without using your prior knowledge')],                         # 4
     [('people are friends',), ('airports are connected',)],                                        # 5
     [(),()]]
INSTR_TRAIN = 'Now you will see which {}, and which are not. Press space to move on to the next group. ' \
              'Once you have seen all {}, you will be tested on how well you remember this information. ' \
              'Press the space bar to begin.'
INSTR_TRAIN_FILLINGS = [('people are friends', 'people'),
                        ('airports are connected by a direct flight', 'airports')]
INSTR_TEST = 'You have just seen all {}. Now try to remember which {}, and which are not. You will see ' \
             'two {} at a time. Answer whether or not they are {} by pressing the Right or Left arrow key on the ' \
             'keyboard, respectively.\n\n' \
             'After you answer, you will be told if you were correct or incorrect, and whether or not they are {}.'
INSTR_TEST_FILLINGS = [('people', 'people are friends', 'people', 'friends', 'friends'),
                       ('airports', 'airports are connected by a direct flight', 'airports',
                        'connected by a direct flight', 'connected by a direct flight')]
INSTR_PRACTICE = 'This is a practice round for you to get used to the task. '\
                 'As such, you will not earn or lose any points this rounds.'
INSTR_POINTS = 'From now on, you\'ll also see the points you earned in the current round.\n\n' \
               'You will earn 1 point for a correct answer, and lose 3 points for an incorrect answer.'
TRAIN_TEXT = 'This {} is {} the following {}:'
TRAIN_TEXT_FILLINGS_POS = [('person', 'friends with', 'people'),
                           ('airport', 'connected to', 'airports by a direct flight')]
TRAIN_TEXT_FILLINGS_NEG = [('person', 'NOT friends with', 'people'),
                           ('airport', 'NOT connected to', 'airports by a direct flight')]
FEEDBACK_RIGHT = 'Correct!'
FEEDBACK_WRONG = 'Incorrect'
FEEDBACK_FRIEND_TEXTS = ['These two people ARE friends.',
                         'These two airports ARE connected']
FEEDBACK_FOE_TEXTS = ['These two people are NOT friends.',
                      'These two airports are NOT connected']
INSTR_END = 'Thank you!\n\nThis part of the task is finished. Please tell the experimenter. ' \
            'They will get you started on the next part of the study.'
CONT_TEXT = 'Press space to continue'
POINTS_TEXT = 'Total points: %d'

# Networks
EDGES = [
    {   # Network A
        9: [(0, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5),
            (3, 6), (4, 5), (6, 7), (6, 8), (7, 8)],
        15: [(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (6, 7), (7, 8), (7, 9),
             (7, 10), (7, 11), (8, 9), (8, 10), (8, 11), (9, 10), (9, 11), (10, 11), (9, 12),
             (12, 13), (12, 14), (13, 14)]},
    {   # Network B
        9: [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (4, 7), (7, 8)],
        15: [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (4, 7), (7, 8), (9, 10), (10, 11),
             (11, 12), (12, 13), (13, 14)]
    }]
