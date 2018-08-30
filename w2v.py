from time import gmtime, strftime, sleep

import logging, gensim
import pandas as pd
import numpy as np

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gio


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Simple Word2Vec')
        self.set_border_width(20)
        self.set_size_request(800, 600)

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        self.set_titlebar(headerbar)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(300)

        self.create_home()
        stack.add_titled(self.home, 'home', 'Word2Vec')

        self.create_info()
        stack.add_titled(self.info, 'info', 'Info')

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack, True, True, 0)

        headerbar.pack_start(stack_switcher)

    def create_home(self):
        self.home = Gtk.Box(spacing = 20)
        self.home.set_homogeneous(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
        vbox.set_homogeneous(False)
        self.home.pack_start(vbox, True, True, 0)

        label = Gtk.Label('Input your text in the field below. Please make sure that:\n'
        '1. There is one item per line\n'
        '2. Items made of multiple words must be separated with by an underscore ( _ ), not a space\n'
        '3. All items are lowercase')
        label.set_line_wrap(True)
        vbox.pack_start(label, False, False, 0)

        self.model = None #Reserving beforehand the variable

        ###---Input Box---###
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_min_content_height(250)
        scrolledwindow.set_vexpand(True)

        vbox.pack_start(scrolledwindow, True, True, 0)
        
        self.textbox = Gtk.TextView()
        self.textbuffer = self.textbox.get_buffer()
        self.textbuffer.set_text('hello_world')
        scrolledwindow.add(self.textbox)

        ###---Log Box---###
        #TODO: Find a way in insert time and date into log
        #TODO: Learn how to make the window scroll by itself

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_max_content_height(250)
        scrolledwindow.set_min_content_height(250)
        scrolledwindow.set_hexpand(True)
        vbox.pack_start(scrolledwindow, False, False, 0)

        self.logbox = Gtk.TextView(monospace = True)
        self.logbuffer = self.logbox.get_buffer()
        self.logbuffer.set_text(log_messages(0))
        scrolledwindow.add(self.logbox)
        
        ###---Buttons---###
        start_model = Gtk.Switch()
        start_model.connect("notify::active", self.load_model)
        start_model.set_active(False)

        query_submit = Gtk.Button(label='Submit')
        query_submit.connect("clicked", self.query_model)

        self.file_browse = Gtk.FileChooserButton()

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 20)
        vbox.pack_end(hbox, False, False, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
        vbox.set_homogeneous(False)
        hbox.pack_start(vbox, True, True, 0)
        
        vbox.pack_start(start_model, False, True, 0)
        vbox.pack_start(self.file_browse, False, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
        vbox.set_homogeneous(False)
        hbox.pack_start(vbox, True, True, 0)

        vbox.pack_start(query_submit, True, True, 0)

    def create_info(self):
        self.info = Gtk.Box(spacing=10)
        self.info.set_homogeneous(False)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        vbox.set_homogeneous(False)
        self.info.pack_start(vbox, True, True, 0)

        text = ['SW2V (v0.1)',
        'This project is a simple GTK3 graphical user interface (GUI) for gensim\'s Word2Vec.',
        'Its purpose is to streamline (at least a bit) the process of querying a W2V model.\nCurrently, it only outputs the cosine similarity between inputed terms.',
        'How to use the software:\n1. Input the terms you want to research in the text field\n2. Load the (appropriate) W2V model\n3. Grab a coffee and wait for the model to load\n4. Press submit and open the generated CSV file (it is in the \'exports\' folder)',
        'Made by Tudor Paisa | Licensed under GPL v2 | 2018']

        label = Gtk.Label(text[0])
        vbox.pack_start(label, True, True, 0)

        text_body = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        text_body.set_homogeneous(False)
        vbox.pack_start(text_body, True, True, 0)

        label = Gtk.Label(text[1]+'\n'+text[2]+'\n'+text[3])
        label.set_line_wrap(True)
        text_body.pack_start(label, False, False, 0)

        label = Gtk.Label(text[len(text)-1])
        vbox.pack_end(label, True, True, 0)

    def load_model(self, switch, gparam):
        if switch.get_active():
            self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(1))
            sleep(5) #To give enough time for the message to pop on the screen
            file_location = self.file_browse.get_uri()
            if file_location is not None:
                try:
                    self.model = gensim.models.KeyedVectors.load_word2vec_format(file_location)
                    self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(2))
                except ValueError:
                    self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(8))
                    switch.set_state(False)
            else:
                self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(7))
                switch.set_state(False)
        else:
            try:
                self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(3))
                del self.model
                self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(4))
            except:
                self.model = None

    def query_model(self, button):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        terms = self.textbuffer.get_text(start, end, False)
        if self.model is not None:
            print('[ ]', strftime('%H:%M:%S', gmtime()), ' Querying the model...')
            self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(5))
            query_similarity(terms, self.model)
            self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(6))
        else:
            self.logbuffer.insert(self.logbuffer.get_end_iter(), log_messages(7))

def query_similarity(terms, model):
    query = terms.splitlines()
    l = []

    for i in query:
        ls = []

        for j in query:
            try:
                ls.append(round(model.similarity(str(i), str(j)), 8))
            except:
                ls.append('0')
        
        l.append(ls)
        c_arr = np.array(l)

    print('[x]', strftime('%H:%M:%S', gmtime()), ' Cosines generated')
    print('[ ]', strftime('%H:%M:%S', gmtime()), ' Saving cosines...')

    df = pd.DataFrame(c_arr, index = query, columns = query)
    csv_location = 'exports/' + strftime('%y%m%d_%H%M%S') + ' - W2V_Cosines.csv'
    df.to_csv(csv_location)

    print('[x]', strftime('%H:%M:%S', gmtime()), ' Cosines saved')
    print(df.head())

def log_messages(idx):
    log = ['[!] Please load the model before submitting',
    '\n[ ] Loading model...',
    '\n[X] Model loaded! You can query now.',
    '\n[ ] Closing model...',
    '\n[X] Model successfully closed!',
    '\n[ ] Querying the model...',
    '\n[X] Finished! You can check the \'exports\' folder to see the results.',
    '\n[!] Error: Missing model. Please load the Word2Vec model first',
    '\n[!] Error: Could not load file. Is it a Word2Vec model?']
    return log[idx]

win = MainWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()