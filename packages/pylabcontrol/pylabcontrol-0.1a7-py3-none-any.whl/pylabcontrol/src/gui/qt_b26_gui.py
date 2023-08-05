# This file is part of pylabcontrol, software for laboratory equipment control for scientific experiments.
# Copyright (C) <2016>  Arthur Safira, Jan Gieseler, Aaron Kabcenell
#
# pylabcontrol is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylabcontrol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylabcontrol.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.uic import loadUiType
from pylabcontrol.core import Parameter, Instrument, Script, Probe
from pylabcontrol.core.script_iterator import ScriptIterator
from pylabcontrol.core.read_probes import ReadProbes
from pylabcontrol.gui import B26QTreeItem, LoadDialog, LoadDialogProbes
from pylabcontrol.scripts.select_points import SelectPoints
from pylabcontrol.core.read_write_functions import load_b26_file

import os.path
import numpy as np
import json as json
from PyQt5.QtCore import QThread, pyqtSlot
import webbrowser

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as Canvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import datetime
from collections import deque
import operator
from functools import reduce




# load the basic old_gui either from .ui file or from precompiled .py file
try:
    # import external_modules.matplotlibwidget
    Ui_MainWindow, QMainWindow = loadUiType('basic_application_window.ui') # with this we don't have to convert the .ui file into a python file!
except (ImportError, IOError):
    # load precompiled old_gui, to complite run pyqt_uic basic_application_window.ui -o basic_application_window.py
    from pylabcontrol.gui.compiled_ui_files.basic_application_window import Ui_MainWindow
    from PyQt5.QtWidgets import QMainWindow
    print('Warning: on-the-fly conversion of basic_application_window.ui file failed, loaded .py file instead.\n')


class CustomEventFilter(QtCore.QObject):
    def eventFilter(self, QObject, QEvent):
        if (QEvent.type() == QtCore.QEvent.Wheel):
            QEvent.ignore()
            return True

        return QtWidgets.QWidget.eventFilter(QObject, QEvent)


class ControlMainWindow(QMainWindow, Ui_MainWindow):

    # application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # application_path = os.path.dirname(application_path) # go one level lower
    application_path = os.path.abspath(os.path.curdir)

    _DEFAULT_CONFIG = {
        # "tmp_folder": "../../b26_tmp",
        "data_folder": os.path.join(application_path, "user_data", "data"),
        "probes_folder": os.path.join(application_path, "user_data", "probes_auto_generated"),
        "instrument_folder": os.path.join(application_path, "user_data", "instruments_auto_generated"),
        "scripts_folder": os.path.join(application_path, "user_data", "scripts_auto_generated"),
        "probes_log_folder": os.path.join(application_path, "user_data", "b26_tmp"),
        "settings_file": os.path.join(application_path, "user_data", "pythonlab_config")
    }


    startup_msg = '\n\n\
    ======================================================\n\
    =============== Starting B26 Python LAB  =============\n\
    ======================================================\n\n'

    def __init__(self, filename=None):
        """
        MainWindow(intruments, scripts, probes)
            - intruments: depth 1 dictionary where keys are instrument names and keys are instrument classes
            - scripts: depth 1 dictionary where keys are script names and keys are script classes
            - probes: depth 1 dictionary where to be decided....?

        MainWindow(settings_file)
            - settings_file is the path to a json file that contains all the settings for the old_gui

        Returns:

        """

        print((self.startup_msg))
        self.config_filename = None
        super(ControlMainWindow, self).__init__()
        self.setupUi(self)

        def setup_trees():
            # COMMENT_ME

            # define data container
            self.history = deque(maxlen=500)  # history of executed commands
            self.history_model = QtGui.QStandardItemModel(self.list_history)
            self.list_history.setModel(self.history_model)
            self.list_history.show()

            self.tree_scripts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tree_probes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tree_settings.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            self.tree_gui_settings.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tree_gui_settings.doubleClicked.connect(self.edit_tree_item)

            self.current_script = None
            self.probe_to_plot = None

            # create models for tree structures, the models reflect the data
            self.tree_dataset_model = QtGui.QStandardItemModel()
            self.tree_dataset.setModel(self.tree_dataset_model)
            self.tree_dataset_model.setHorizontalHeaderLabels(['time', 'name (tag)', 'type (script)'])

            # create models for tree structures, the models reflect the data
            self.tree_gui_settings_model = QtGui.QStandardItemModel()
            self.tree_gui_settings.setModel(self.tree_gui_settings_model)
            self.tree_gui_settings_model.setHorizontalHeaderLabels(['parameter', 'value'])

            self.tree_scripts.header().setStretchLastSection(True)
        def connect_controls():
            # COMMENT_ME
            # =============================================================
            # ===== LINK WIDGETS TO FUNCTIONS =============================
            # =============================================================

            # link buttons to old_functions
            self.btn_start_script.clicked.connect(self.btn_clicked)
            self.btn_stop_script.clicked.connect(self.btn_clicked)
            self.btn_skip_subscript.clicked.connect(self.btn_clicked)
            self.btn_validate_script.clicked.connect(self.btn_clicked)
            # self.btn_plot_script.clicked.connect(self.btn_clicked)
            # self.btn_plot_probe.clicked.connect(self.btn_clicked)
            self.btn_store_script_data.clicked.connect(self.btn_clicked)
            # self.btn_plot_data.clicked.connect(self.btn_clicked)
            self.btn_save_data.clicked.connect(self.btn_clicked)
            self.btn_delete_data.clicked.connect(self.btn_clicked)


            self.btn_save_gui.triggered.connect(self.btn_clicked)
            self.btn_load_gui.triggered.connect(self.btn_clicked)
            self.btn_about.triggered.connect(self.btn_clicked)
            self.btn_exit.triggered.connect(self.close)

            self.actionSave.triggered.connect(self.btn_clicked)
            self.actionGo_to_pylabcontrol_GitHub_page.triggered.connect(self.btn_clicked)

            self.btn_load_instruments.clicked.connect(self.btn_clicked)
            self.btn_load_scripts.clicked.connect(self.btn_clicked)
            self.btn_load_probes.clicked.connect(self.btn_clicked)

            # Helper function to make only column 1 editable
            def onScriptParamClick(item, column):
                tree = item.treeWidget()
                if column == 1 and not isinstance(item.value, (Script, Instrument)) and not item.is_point():
                    # self.tree_scripts.editItem(item, column)
                    tree.editItem(item, column)

            # tree structures
            self.tree_scripts.itemClicked.connect(
                lambda: onScriptParamClick(self.tree_scripts.currentItem(), self.tree_scripts.currentColumn()))
            self.tree_scripts.itemChanged.connect(lambda: self.update_parameters(self.tree_scripts))
            self.tree_scripts.itemClicked.connect(self.btn_clicked)
            # self.tree_scripts.installEventFilter(self)
            # QtWidgets.QTreeWidget.installEventFilter(self)


            self.tabWidget.currentChanged.connect(lambda : self.switch_tab())
            self.tree_dataset.clicked.connect(lambda: self.btn_clicked())

            self.tree_settings.itemClicked.connect(
                lambda: onScriptParamClick(self.tree_settings.currentItem(), self.tree_settings.currentColumn()))
            self.tree_settings.itemChanged.connect(lambda: self.update_parameters(self.tree_settings))
            self.tree_settings.itemExpanded.connect(lambda: self.refresh_instruments())


            # set the log_filename when checking loggin
            self.chk_probe_log.toggled.connect(lambda: self.set_probe_file_name(self.chk_probe_log.isChecked()))
            self.chk_probe_plot.toggled.connect(self.btn_clicked)

            self.chk_show_all.toggled.connect(self._show_hide_parameter)

        self.create_figures()


        # create a "delegate" --- an editor that uses our new Editor Factory when creating editors,
        # and use that for tree_scripts
        # needed to avoid rounding of numbers
        delegate = QtWidgets.QStyledItemDelegate()
        new_factory = CustomEditorFactory()
        delegate.setItemEditorFactory(new_factory)
        self.tree_scripts.setItemDelegate(delegate)
        setup_trees()

        connect_controls()
        if not os.path.exists(filename):
            dialog_dir = ''

            # set path to home path
            for x in ['HOME', 'HOMEPATH']:
                if x in os.environ:
                    dialog_dir = os.environ[x]

            # set to path of requested file
            if os.path.exists(os.path.dirname(filename)):
                dialog_dir = filename

            # we use the save dialog here so that we can also create a new file (the default config)
            # however, as a consequence if the user selects a file that already exists, such as a valid config file
            # the dialog asks if the file should be over-written (I guess that is ok, because this is what happens
            # when you close the gui)
            filename = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Unvalid Config File. Select Config.',
                                                             dialog_dir,'b26 files (*.b26)')[0])
            if filename == '':
                #todo: create all the settings outside of init and only then start loading the gui!
                raise ValueError
            # started to work on custom dialog, but this is not finished yet
            # keep the code for now:

            # === begin custom dialog ====
            # dialog = QtWidgets.QFileDialog(self)
            # dialog.setNameFilter('b26 files (*.b26)')
            # dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            # dialog.setDirectory(dialog_dir)
            # dialog.setWindowTitle('Unvalid Config File. Select Config.')
            # dialog.setParent(self)
            # filename = str(dialog.open())
            # print(filename)
            # === end custom dialog ====
            self.instruments = {}
            self.scripts = {}
            self.probes = {}
            self.gui_settings = {'scripts_folder': '', 'data_folder': ''}

        self.config_filename = filename

        self.load_config(self.config_filename)

        self.data_sets = {}  # todo: load datasets from tmp folder
        self.read_probes = ReadProbes(self.probes)
        self.tabWidget.setCurrentIndex(0) # always show the script tab

        # == create a thread for the scripts ==
        self.script_thread = QThread()
        self._last_progress_update = None # used to keep track of status updates, to block updates when they occur to often

        self.chk_show_all.setChecked(True)
        self.actionSave.setShortcut(QtGui.QKeySequence.Save)
        self.list_history.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def closeEvent(self, event):
        """
        things to be done when gui closes, like save the settings
        """

        self.script_thread.quit()
        self.read_probes.quit()
        if self.config_filename:
            fname = self.config_filename
            self.save_config(fname)

        event.accept()

        print('\n\n======================================================')
        print('================= Closing B26 Python LAB =============')
        print('======================================================\n\n')

    def eventFilter(self, object, event):
        """

        TEMPORARY / UNDER DEVELOPMENT

        THIS IS TO ALLOW COPYING OF PARAMETERS VIA DRAP AND DROP

        Args:
            object:
            event:

        Returns:

        """
        if (object is self.tree_scripts):
            # print('XXXXXXX = event in scripts', event.type(),
            #       QtCore.QEvent.DragEnter, QtCore.QEvent.DragMove, QtCore.QEvent.DragLeave)
            if (event.type() == QtCore.QEvent.ChildAdded):
                item = self.tree_scripts.selectedItems()[0]
                if not isinstance(item.value, Script):
                    print('ONLY SCRIPTS CAN BE DRAGGED')
                    return False
                print(('XXX ChildAdded', self.tree_scripts.selectedItems()[0].name))



                # if event.mimeData().hasUrls():
                #     event.accept()  # must accept the dragEnterEvent or else the dropEvent can't occur !!!
                #     print "accept"
                # else:
                #     event.ignore()
                #     print "ignore"
            if (event.type() == QtCore.QEvent.ChildRemoved):
                print(('XXX ChildRemoved', self.tree_scripts.selectedItems()[0].name))
            if (event.type() == QtCore.QEvent.Drop):
                print('XXX Drop')
                # if event.mimeData().hasUrls():  # if file or link is dropped
                #     urlcount = len(event.mimeData().urls())  # count number of drops
                #     url = event.mimeData().urls()[0]  # get first url
                #     object.setText(url.toString())  # assign first url to editline
                #     # event.accept()  # doesnt appear to be needed
            return False  # lets the event continue to the edit

        return False


    def set_probe_file_name(self, checked):
        """
        sets the filename to which the probe logging function will write
        Args:
            checked: boolean (True: opens file) (False: closes file)
        """
        if checked:
            file_name = os.path.join(self.gui_settings['probes_log_folder'], '{:s}_probes.csv'.format(datetime.datetime.now().strftime('%y%m%d-%H_%M_%S')))
            if os.path.isfile(file_name) == False:
                self.probe_file = open(file_name, 'a')
                new_values = self.read_probes.probes_values
                header = ','.join(list(np.array([['{:s} ({:s})'.format(p, instr) for p in list(p_dict.keys())] for instr, p_dict in new_values.items()]).flatten()))
                self.probe_file.write('{:s}\n'.format(header))
        else:
            self.probe_file.close()



    def switch_tab(self):
        """
        takes care of the action that happen when switching between tabs
        e.g. activates and deactives probes
        """
        current_tab = str(self.tabWidget.tabText(self.tabWidget.currentIndex()))
        if self.current_script is None:
            if current_tab == 'Probes':
                self.read_probes.start()
                self.read_probes.updateProgress.connect(self.update_probes)
            else:
                try:
                    self.read_probes.updateProgress.disconnect()
                    self.read_probes.quit()
                except TypeError:
                    pass

            if current_tab == 'Instruments':
                self.refresh_instruments()

        else:
            self.log('updating probes / instruments disabled while script is running!')

    def refresh_instruments(self):
        """
        if self.tree_settings has been expanded, ask instruments for their actual values
        """
        def list_access_nested_dict(dict, somelist):
            """
            Allows one to use a list to access a nested dictionary, for example:
            listAccessNestedDict({'a': {'b': 1}}, ['a', 'b']) returns 1
            Args:
                dict:
                somelist:

            Returns:

            """
            return reduce(operator.getitem, somelist, dict)

        def update(item):
            if item.isExpanded():
                for index in range(item.childCount()):
                    child = item.child(index)

                    if child.childCount() == 0:
                        instrument, path_to_instrument = child.get_instrument()
                        path_to_instrument.reverse()
                        try: #check if item is in probes
                            value = instrument.read_probes(path_to_instrument[-1])
                        except AssertionError: #if item not in probes, get value from settings instead
                            value = list_access_nested_dict(instrument.settings, path_to_instrument)
                        child.value = value
                    else:
                        update(child)

        #need to block signals during update so that tree.itemChanged doesn't fire and the gui doesn't try to
        #reupdate the instruments to their current value
        self.tree_settings.blockSignals(True)

        for index in range(self.tree_settings.topLevelItemCount()):
            instrument = self.tree_settings.topLevelItem(index)
            update(instrument)

        self.tree_settings.blockSignals(False)


    def plot_clicked(self, mouse_event):
        """
        gets activated when the user clicks on a plot
        Args:
            mouse_event:
        """
        if isinstance(self.current_script, SelectPoints) and self.current_script.is_running:
            if (not (mouse_event.xdata == None)):
                if (mouse_event.button == 1):
                    pt = np.array([mouse_event.xdata, mouse_event.ydata])
                    self.current_script.toggle_NV(pt)
                    self.current_script.plot([self.matplotlibwidget_1.figure])
                    self.matplotlibwidget_1.draw()

        item = self.tree_scripts.currentItem()

        if item is not None:
            if item.is_point():
                item_x = item.child(1)
                if mouse_event.xdata is not None:
                    self.tree_scripts.setCurrentItem(item_x)
                    item_x.value = float(mouse_event.xdata)
                    item_x.setText(1, '{:0.3f}'.format(float(mouse_event.xdata)))
                item_y = item.child(0)
                if mouse_event.ydata is not None:
                    self.tree_scripts.setCurrentItem(item_y)
                    item_y.value = float(mouse_event.ydata)
                    item_y.setText(1, '{:0.3f}'.format(float(mouse_event.ydata)))

                # focus back on item
                self.tree_scripts.setCurrentItem(item)
            else:
                if item.parent() is not None:
                    if item.parent().is_point():
                        if item == item.parent().child(1):
                            if mouse_event.xdata is not None:
                                item.setData(1, 2, float(mouse_event.xdata))
                        if item == item.parent().child(0):
                            if mouse_event.ydata is not None:
                                item.setData(1, 2, float(mouse_event.ydata))

    def get_time(self):
        """
        Returns: the current time as a formated string
        """
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    def log(self, msg):
        """
        log function
        Args:
            msg: the text message to be logged
        """

        time = self.get_time()

        msg = "{:s}\t {:s}".format(time, msg)

        self.history.append(msg)
        self.history_model.insertRow(0, QtGui.QStandardItem(msg))

    def create_figures(self):
        """
        creates the maplotlib figures]
        self.matplotlibwidget_1
        self.matplotlibwidget_2
        and toolbars
        self.mpl_toolbar_1
        self.mpl_toolbar_2
        Returns:

        """


        try:
            self.horizontalLayout_14.removeWidget(self.matplotlibwidget_1)
            self.matplotlibwidget_1.close()
        except AttributeError:
            pass
        try:
            self.horizontalLayout_15.removeWidget(self.matplotlibwidget_2)
            self.matplotlibwidget_2.close()
        except AttributeError:
            pass
        self.matplotlibwidget_2 = MatplotlibWidget(self.plot_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matplotlibwidget_2.sizePolicy().hasHeightForWidth())
        self.matplotlibwidget_2.setSizePolicy(sizePolicy)
        self.matplotlibwidget_2.setMinimumSize(QtCore.QSize(200, 200))
        self.matplotlibwidget_2.setObjectName("matplotlibwidget_2")
        self.horizontalLayout_16.addWidget(self.matplotlibwidget_2)
        self.matplotlibwidget_1 = MatplotlibWidget(self.plot_1)
        self.matplotlibwidget_1.setMinimumSize(QtCore.QSize(200, 200))
        self.matplotlibwidget_1.setObjectName("matplotlibwidget_1")
        self.horizontalLayout_15.addWidget(self.matplotlibwidget_1)

        self.matplotlibwidget_1.mpl_connect('button_press_event', self.plot_clicked)
        self.matplotlibwidget_2.mpl_connect('button_press_event', self.plot_clicked)

        # adds a toolbar to the plots
        self.mpl_toolbar_1 = NavigationToolbar(self.matplotlibwidget_1.canvas, self.toolbar_space_1)
        self.mpl_toolbar_2 = NavigationToolbar(self.matplotlibwidget_2.canvas, self.toolbar_space_2)
        self.horizontalLayout_9.addWidget(self.mpl_toolbar_2)
        self.horizontalLayout_14.addWidget(self.mpl_toolbar_1)

        self.matplotlibwidget_1.figure.set_tight_layout(True)
        self.matplotlibwidget_2.figure.set_tight_layout(True)

    def load_scripts(self):
            """
            opens file dialog to load scripts into gui
            """


            # update scripts so that current settings do not get lost
            for index in range(self.tree_scripts.topLevelItemCount()):
                script_item = self.tree_scripts.topLevelItem(index)
                self.update_script_from_item(script_item)


            dialog = LoadDialog(elements_type="scripts", elements_old=self.scripts,
                                filename=self.gui_settings['scripts_folder'])
            if dialog.exec_():
                self.gui_settings['scripts_folder'] = str(dialog.txt_probe_log_path.text())
                scripts = dialog.get_values()
                added_scripts = set(scripts.keys()) - set(self.scripts.keys())
                removed_scripts = set(self.scripts.keys()) - set(scripts.keys())

                if 'data_folder' in list(self.gui_settings.keys()) and os.path.exists(self.gui_settings['data_folder']):
                    data_folder_name = self.gui_settings['data_folder']
                else:
                    data_folder_name = None

                # create instances of new instruments/scripts
                self.scripts, loaded_failed, self.instruments = Script.load_and_append(
                    script_dict={name: scripts[name] for name in added_scripts},
                    scripts=self.scripts,
                    instruments=self.instruments,
                    log_function=self.log,
                    data_path=data_folder_name)

                # delete instances of new instruments/scripts that have been deselected
                for name in removed_scripts:
                    del self.scripts[name]

    def btn_clicked(self):
        """
        slot to which connect buttons
        """
        sender = self.sender()
        self.probe_to_plot = None

        def start_button():
            """
            starts the selected script
            """
            item = self.tree_scripts.currentItem()

            # BROKEN 20170109: repeatedly erases updates to gui
            # self.expanded_items = []
            # for index in range(self.tree_scripts.topLevelItemCount()):
            #     someitem = self.tree_scripts.topLevelItem(index)
            #     if someitem.isExpanded():
            #         self.expanded_items.append(someitem.name)
            self.script_start_time = datetime.datetime.now()


            if item is not None:
                # get script and update settings from tree
                self.running_item = item
                script, path_to_script, script_item = item.get_script()

                self.update_script_from_item(script_item)

                self.log('starting {:s}'.format(script.name))

                # put script onto script thread
                print('================================================')
                print(('===== starting {:s}'.format(script.name)))
                print('================================================')
                script_thread = self.script_thread

                def move_to_worker_thread(script):

                    script.moveToThread(script_thread)

                    # move also the subscript to the worker thread
                    for subscript in list(script.scripts.values()):
                        move_to_worker_thread(subscript)

                move_to_worker_thread(script)

                script.updateProgress.connect(self.update_status) # connect update signal of script to update slot of gui
                script_thread.started.connect(script.run) # causes the script to start upon starting the thread
                script.finished.connect(script_thread.quit)  # clean up. quit thread after script is finished
                script.finished.connect(self.script_finished) # connect finished signal of script to finished slot of gui

                # start thread, i.e. script
                script_thread.start()

                self.current_script = script
                self.btn_start_script.setEnabled(False)
                # self.tabWidget.setEnabled(False)

                if isinstance(self.current_script, ScriptIterator):
                    self.btn_skip_subscript.setEnabled(True)


            else:
                self.log('User tried to run a script without one selected.')

        def stop_button():
            """
            stops the current script
            """
            if self.current_script is not None and self.current_script.is_running:
                self.current_script.stop()
            else:
                self.log('User clicked stop, but there isn\'t anything running...this is awkward. Re-enabling start button anyway.')
            self.btn_start_script.setEnabled(True)

        def skip_button():
            """
            Skips to the next script if the current script is a Iterator script
            """
            if self.current_script is not None and self.current_script.is_running and isinstance(self.current_script,
                                                                                                 ScriptIterator):
                self.current_script.skip_next()
            else:
                self.log('User clicked skip, but there isn\'t a iterator script running...this is awkward.')

        def validate_button():
            """
            validates the selected script
            """
            item = self.tree_scripts.currentItem()

            if item is not None:
                script, path_to_script, script_item = item.get_script()
                self.update_script_from_item(script_item)
                script.is_valid()
                script.plot_validate([self.matplotlibwidget_1.figure, self.matplotlibwidget_2.figure])
                self.matplotlibwidget_1.draw()
                self.matplotlibwidget_2.draw()

        def store_script_data():
            """
            updates the internal self.data_sets with selected script and updates tree self.fill_dataset_tree
            """
            item = self.tree_scripts.currentItem()
            if item is not None:
                script, path_to_script, _ = item.get_script()
                script_copy = script.duplicate()
                time_tag = script.start_time.strftime('%y%m%d-%H_%M_%S')

                self.data_sets.update({time_tag : script_copy})

                self.fill_dataset_tree(self.tree_dataset, self.data_sets)

        def save_data():
            """"
            saves the selected script (where is contained in the script itself)
            """
            indecies = self.tree_dataset.selectedIndexes()
            model = indecies[0].model()
            rows = list(set([index.row()for index in indecies]))

            for row in rows:
                time_tag = str(model.itemFromIndex(model.index(row, 0)).text())
                name_tag = str(model.itemFromIndex(model.index(row, 1)).text())
                path = self.gui_settings['data_folder']
                script = self.data_sets[time_tag]
                script.update({'tag' : name_tag, 'path': path})
                script.save_data()
                script.save_image_to_disk()
                script.save_b26()
                script.save_log()

        def delete_data():
            """
            deletes the data from the dataset
            Returns:
            """
            indecies = self.tree_dataset.selectedIndexes()
            model = indecies[0].model()
            rows = list(set([index.row()for index in indecies]))

            for row in rows:
                time_tag = str(model.itemFromIndex(model.index(row, 0)).text())
                del self.data_sets[time_tag]

                model.removeRows(row,1)

        def load_probes():
            """
            opens file dialog to load probes into gui
            """

            # if the probe has never been started it can not be disconnected so we catch that error
            try:
                self.read_probes.updateProgress.disconnect()
                self.read_probes.quit()
                # self.read_probes.stop()
            except RuntimeError:
                pass
            dialog = LoadDialogProbes(probes_old=self.probes, filename=self.gui_settings['probes_folder'])
            if dialog.exec_():
                self.gui_settings['probes_folder'] = str(dialog.txt_probe_log_path.text())
                probes = dialog.getValues()
                added_instruments = list(set(probes.keys()) - set(self.probes.keys()))
                removed_instruments = list(set(self.probes.keys()) - set(probes.keys()))
                # create instances of new probes
                self.probes, loaded_failed, self.instruments = Probe.load_and_append(
                    probe_dict=probes,
                    probes={},
                    instruments=self.instruments)
                if not loaded_failed:
                    print(('WARNING following probes could not be loaded', loaded_failed, len(loaded_failed)))


                # restart the readprobes thread
                del self.read_probes
                self.read_probes = ReadProbes(self.probes)
                self.read_probes.start()
                self.tree_probes.clear() # clear tree because the probe might have changed
                self.read_probes.updateProgress.connect(self.update_probes)
                self.tree_probes.expandAll()

        def load_instruments():
            """
            opens file dialog to load instruments into gui
            """
            if 'instrument_folder' in self.gui_settings:
                dialog = LoadDialog(elements_type="instruments", elements_old=self.instruments,
                                    filename=self.gui_settings['instrument_folder'])

            else:
                dialog = LoadDialog(elements_type="instruments", elements_old=self.instruments)

            if dialog.exec_():
                self.gui_settings['instrument_folder'] = str(dialog.txt_probe_log_path.text())
                instruments = dialog.get_values()
                added_instruments = set(instruments.keys()) - set(self.instruments.keys())
                removed_instruments = set(self.instruments.keys()) - set(instruments.keys())
                # print('added_instruments', {name: instruments[name] for name in added_instruments})

                # create instances of new instruments
                self.instruments, loaded_failed = Instrument.load_and_append(
                    {name: instruments[name] for name in added_instruments}, self.instruments)
                if len(loaded_failed)>0:
                    print(('WARNING following instrument could not be loaded', loaded_failed))
                # delete instances of new instruments/scripts that have been deselected
                for name in removed_instruments:
                    del self.instruments[name]

        def plot_data(sender):
            """
            plots the data of the selected script
            """
            if sender == self.tree_dataset:
                index = self.tree_dataset.selectedIndexes()[0]
                model = index.model()
                time_tag = str(model.itemFromIndex(model.index(index.row(), 0)).text())
                script = self.data_sets[time_tag]
                self.plot_script(script)
            elif sender == self.tree_scripts:
                item = self.tree_scripts.currentItem()
                if item is not None:
                    script, path_to_script, _ = item.get_script()
                # only plot if script has been selected but not if a parameter has been selected
                if path_to_script == []:
                    self.plot_script(script)

        def save():
            self.save_config(self.config_filename)

        if sender is self.btn_start_script:
            start_button()
        elif sender is self.btn_stop_script:
            stop_button()
        elif sender is self.btn_skip_subscript:
            skip_button()
        elif sender is self.btn_validate_script:
            validate_button()
        elif sender in (self.tree_dataset, self.tree_scripts):
            plot_data(sender)
        elif sender is self.btn_store_script_data:
            store_script_data()
        elif sender is self.btn_save_data:
            save_data()
        elif sender is self.btn_delete_data:
            delete_data()
        # elif sender is self.btn_plot_probe:
        elif sender is self.chk_probe_plot:
            if self.chk_probe_plot.isChecked():
                item = self.tree_probes.currentItem()
                if item is not None:
                    if item.name in self.probes:
                        #selected item is an instrument not a probe, maybe plot all the probes...
                        self.log('Can\'t plot, No probe selected. Select probe and try again!')
                    else:
                        instrument = item.parent().name
                        self.probe_to_plot = self.probes[instrument][item.name]
                else:
                    self.log('Can\'t plot, No probe selected. Select probe and try again!')
            else:
                self.probe_to_plot = None
        elif sender is self.btn_save_gui:
            # get filename
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save gui settings to file', self.gui_settings['data_folder']) # filter = '.b26gui'
            self.save_config(fname[0])
        elif sender is self.btn_load_gui:
            # get filename
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Load gui settings from file',  self.gui_settings['data_folder'])
            # self.load_settings(fname)
            self.load_config(fname[0])
        elif sender is self.btn_about:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("pylabcontrol: Laboratory Equipment Control for Scientific Experiments")
            msg.setInformativeText("This software was developed by Arthur Safira, Jan Gieseler, and Aaron Kabcenell at"
                                   "Harvard University. It is licensed under the LPGL licence. For more information,"
                                   "visit the GitHub page at github.com/LISE-B26/pylabcontrol .")
            msg.setWindowTitle("About")
            # msg.setDetailedText("some stuff")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            # msg.buttonClicked.connect(msgbtn)
            retval = msg.exec_()
        # elif (sender is self.btn_load_instruments) or (sender is self.btn_load_scripts):
        elif sender in (self.btn_load_instruments, self.btn_load_scripts, self.btn_load_probes):
            if sender is self.btn_load_instruments:
                load_instruments()
            elif sender is self.btn_load_scripts:
                self.load_scripts()
            elif sender is self.btn_load_probes:
                load_probes()
            # refresh trees
            self.refresh_tree(self.tree_scripts, self.scripts)
            self.refresh_tree(self.tree_settings, self.instruments)
        elif sender is self.actionSave:
            if self.config_filename:
                self.save_config(self.config_filename)
        elif sender is self.actionGo_to_pylabcontrol_GitHub_page:
            webbrowser.open('https://github.com/LISE-B26/pylabcontrol')

    def _show_hide_parameter(self):
        """
        shows or hides parameters
        Returns:

        """

        assert isinstance(self.sender(), QtWidgets.QCheckBox), 'this function should be connected to a check box'

        if self.sender().isChecked():
            self.tree_scripts.setColumnHidden(2, False)
            iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_scripts, QtWidgets.QTreeWidgetItemIterator.Hidden)
            item = iterator.value()
            while item:
                item.setHidden(False)
                item = iterator.value()
                iterator += 1
        else:
            self.tree_scripts.setColumnHidden(2, True)

            iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_scripts, QtWidgets.QTreeWidgetItemIterator.NotHidden)
            item = iterator.value()
            while item:
                if not item.visible:
                    item.setHidden(True)
                item = iterator.value()
                iterator +=1


        self.tree_scripts.setColumnWidth(0, 200)
        self.tree_scripts.setColumnWidth(1, 400)
        self.tree_scripts.setColumnWidth(2, 50)
    def update_parameters(self, treeWidget):
        """
        updates the internal dictionaries for scripts and instruments with values from the respective trees

        treeWidget: the tree from which to update

        """

        if treeWidget == self.tree_settings:

            item = treeWidget.currentItem()



            instrument, path_to_instrument = item.get_instrument()

            # build nested dictionary to update instrument
            dictator = item.value
            for element in path_to_instrument:
                dictator = {element: dictator}

            # get old value from instrument
            old_value = instrument.settings
            path_to_instrument.reverse()
            for element in path_to_instrument:
                old_value = old_value[element]

            # send new value from tree to instrument
            instrument.update(dictator)

            new_value = item.value
            if new_value is not old_value:
                msg = "changed parameter {:s} from {:s} to {:s} on {:s}".format(item.name, str(old_value),
                                                                                str(new_value), instrument.name)
            else:
                msg = "did not change parameter {:s} on {:s}".format(item.name, instrument.name)

            self.log(msg)
        elif treeWidget == self.tree_scripts:

            item = treeWidget.currentItem()
            script, path_to_script, _ = item.get_script()

            # check if changes value is from an instrument
            instrument, path_to_instrument = item.get_instrument()
            if instrument is not None:

                new_value = item.value


                msg = "changed parameter {:s} to {:s} in {:s}".format(item.name,
                                                                                str(new_value),
                                                                                script.name)
            else:
                new_value = item.value
                msg = "changed parameter {:s} to {:s} in {:s}".format(item.name,
                                                                            str(new_value),
                                                                            script.name)
            self.log(msg)

    def plot_script(self, script):
        """
        Calls the plot function of the script, and redraws both plots
        Args:
            script: script to be plotted
        """

        script.plot([self.matplotlibwidget_1.figure, self.matplotlibwidget_2.figure])
        self.matplotlibwidget_1.draw()
        self.matplotlibwidget_2.draw()


    @pyqtSlot(int)
    def update_status(self, progress):
        """
        waits for a signal emitted from a thread and updates the gui
        Args:
            progress:
        Returns:

        """

        # interval at which the gui will be updated, if requests come in faster than they will be ignored
        update_interval = 0.2

        now = datetime.datetime.now()

        if not self._last_progress_update is None and now-self._last_progress_update < datetime.timedelta(seconds=update_interval):
            return

        self._last_progress_update = now

        self.progressBar.setValue(progress)

        script = self.current_script

        # Estimate remaining time if progress has been made
        if progress:
            remaining_time = str(datetime.timedelta(seconds=script.remaining_time.seconds))
            self.lbl_time_estimate.setText('time remaining: {:s}'.format(remaining_time))
        if script is not str(self.tabWidget.tabText(self.tabWidget.currentIndex())).lower() in ['scripts', 'instruments']:
            self.plot_script(script)


    @pyqtSlot()
    def script_finished(self):
        """
        waits for the script to emit the script_finshed signal
        """
        script = self.current_script
        script.updateProgress.disconnect(self.update_status)
        self.script_thread.started.disconnect()
        script.finished.disconnect()

        self.current_script = None

        self.plot_script(script)
        self.progressBar.setValue(100)
        self.btn_start_script.setEnabled(True)
        self.btn_skip_subscript.setEnabled(False)

    def plot_script_validate(self, script):
        """
        checks the plottype of the script and plots it accordingly
        Args:
            script: script to be plotted

        """

        script.plot_validate([self.matplotlibwidget_1.figure, self.matplotlibwidget_2.figure])
        self.matplotlibwidget_1.draw()
        self.matplotlibwidget_2.draw()

    def update_probes(self, progress):
        """
        update the probe tree
        """
        new_values = self.read_probes.probes_values
        probe_count = len(self.read_probes.probes)

        if probe_count > self.tree_probes.topLevelItemCount():
            # when run for the first time, there are no probes in the tree, so we have to fill it first
            self.fill_treewidget(self.tree_probes, new_values)
        else:
            for x in range(probe_count):
                topLvlItem = self.tree_probes.topLevelItem(x)
                for child_id in range(topLvlItem.childCount()):
                    child = topLvlItem.child(child_id)
                    child.value = new_values[topLvlItem.name][child.name]
                    child.setText(1, str(child.value))

        if self.probe_to_plot is not None:
            self.probe_to_plot.plot(self.matplotlibwidget_1.axes)
            self.matplotlibwidget_1.draw()


        if self.chk_probe_log.isChecked():
            data = ','.join(list(np.array([[str(p) for p in list(p_dict.values())] for instr, p_dict in new_values.items()]).flatten()))
            self.probe_file.write('{:s}\n'.format(data))

    def update_script_from_item(self, item):
        """
        updates the script based on the information provided in item

        Args:
            script: script to be updated
            item: B26QTreeItem that contains the new settings of the script

        """

        script, path_to_script, script_item = item.get_script()

        # build dictionary
        # get full information from script
        dictator = list(script_item.to_dict().values())[0]  # there is only one item in the dictionary

        for instrument in list(script.instruments.keys()):
            # update instrument
            script.instruments[instrument]['settings'] = dictator[instrument]['settings']
            # remove instrument
            del dictator[instrument]


        for sub_script_name in list(script.scripts.keys()):
            sub_script_item = script_item.get_subscript(sub_script_name)
            self.update_script_from_item(sub_script_item)
            del dictator[sub_script_name]

        script.update(dictator)
        # update datefolder path
        script.data_path = self.gui_settings['data_folder']

    def fill_treewidget(self, tree, parameters):
        """
        fills a QTreeWidget with nested parameters, in future replace QTreeWidget with QTreeView and call fill_treeview
        Args:
            tree: QtWidgets.QTreeWidget
            parameters: dictionary or Parameter object
            show_all: boolean if true show all parameters, if false only selected ones
        Returns:

        """

        tree.clear()
        assert isinstance(parameters, (dict, Parameter))

        for key, value in parameters.items():
            if isinstance(value, Parameter):
                B26QTreeItem(tree, key, value, parameters.valid_values[key], parameters.info[key])
            else:
                B26QTreeItem(tree, key, value, type(value), '')

    def fill_treeview(self, tree, input_dict):
        """
        fills a treeview with nested parameters
        Args:
            tree: QtWidgets.QTreeView
            parameters: dictionary or Parameter object

        Returns:

        """

        tree.model().removeRows(0, tree.model().rowCount())
        def add_elemet(item, key, value):
            child_name = QtWidgets.QStandardItem(key)
            # child_name.setDragEnabled(False)
            # child_name.setSelectable(False)
            # child_name.setEditable(False)

            if isinstance(value, dict):
                for key_child, value_child in value.items():
                    add_elemet(child_name, key_child, value_child)
                item.appendRow(child_name)
            else:
                child_value = QtWidgets.QStandardItem(str(value))
                # child_value.setDragEnabled(False)
                # child_value.setSelectable(False)
                # child_value.setEditable(False)

                item.appendRow([child_name, child_value])

        for index, (key, value) in enumerate(input_dict.items()):

            if isinstance(value, dict):
                item = QtWidgets.QStandardItem(key)
                for sub_key, sub_value in value.items():
                    add_elemet(item, sub_key, sub_value)
                tree.model().appendRow(item)
            elif isinstance(value, str):
                item = QtGui.QStandardItem(key)
                item_value = QtGui.QStandardItem(value)
                item_value.setEditable(True)
                item_value.setSelectable(True)
                tree.model().appendRow([item, item_value])

    def edit_tree_item(self):
        """
        if sender is self.tree_gui_settings this will open a filedialog and ask for a filepath
        this filepath will be updated in the field of self.tree_gui_settings that has been double clicked
        """

        def open_path_dialog(path):
            """
            opens a file dialog to get the path to a file and
            """
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
            path = dialog.getExistingDirectory(self, 'Select a folder:', path)

            return path

        tree = self.sender()

        if tree == self.tree_gui_settings:

            index = tree.selectedIndexes()[0]
            model = index.model()

            if index.column() == 1:
                path = model.itemFromIndex(index).text()
                path = str(open_path_dialog(path))

                key = str(model.itemFromIndex(model.index(index.row(), 0)).text())

                if path != "":
                    self.gui_settings.update({key : str(path)})
                    self.fill_treeview(tree, self.gui_settings)

    def refresh_tree(self, tree, items):
        """
        refresh trees with current settings
        Args:
            tree: a QtWidgets.QTreeWidget object or a QtWidgets.QTreeView object
            items: dictionary or Parameter items with which to populate the tree
            show_all: boolean if true show all parameters, if false only selected ones
        """

        if tree == self.tree_scripts or tree == self.tree_settings:
            tree.itemChanged.disconnect()
            self.fill_treewidget(tree, items)
            tree.itemChanged.connect(lambda: self.update_parameters(tree))
        elif tree == self.tree_gui_settings:
            self.fill_treeview(tree, items)

    def fill_dataset_tree(self, tree, data_sets):
        """
        fills the tree with data sets where datasets is a dictionary of the form
        Args:
            tree:
            data_sets: a dataset

        Returns:

        """

        tree.model().removeRows(0, tree.model().rowCount())
        for index, (time, script) in enumerate(data_sets.items()):
            name = script.settings['tag']
            type = script.name

            item_time = QtGui.QStandardItem(str(time))
            item_name = QtGui.QStandardItem(str(name))
            item_type = QtGui.QStandardItem(str(type))

            item_time.setSelectable(False)
            item_time.setEditable(False)
            item_type.setSelectable(False)
            item_type.setEditable(False)

            tree.model().appendRow([item_time, item_name, item_type])

    def load_config(self, file_name):
        """
        checks if the file is a valid config file
        Args:
            file_name:

        """

        # load config or default if invalid

        def load_settings(file_name):
            """
            loads a old_gui settings file (a json dictionary)
            - path_to_file: path to file that contains the dictionary

            Returns:
                - instruments: depth 1 dictionary where keys are instrument names and values are instances of instruments
                - scripts:  depth 1 dictionary where keys are script names and values are instances of scripts
                - probes: depth 1 dictionary where to be decided....?
            """

            instruments_loaded = {}
            probes_loaded = {}
            scripts_loaded = {}

            if os.path.isfile(file_name):
                in_data = load_b26_file(file_name)

                instruments = in_data['instruments'] if 'instruments' in in_data else {}
                scripts = in_data['scripts'] if 'scripts' in in_data else {}
                probes = in_data['probes'] if 'probes' in in_data else {}

                instruments_loaded, failed = Instrument.load_and_append(instruments)
                if len(failed) > 0:
                    print(('WARNING! Following instruments could not be loaded: ', failed))

                scripts_loaded, failed, instruments_loaded = Script.load_and_append(
                    script_dict=scripts,
                    instruments=instruments_loaded,
                    log_function=self.log,
                    data_path=self.gui_settings['data_folder'])

                if len(failed) > 0:
                    print(('WARNING! Following scripts could not be loaded: ', failed))

                probes_loaded, failed, instruments_loadeds = Probe.load_and_append(
                    probe_dict=probes,
                    probes=probes_loaded,
                    instruments=instruments_loaded)
            return instruments_loaded, scripts_loaded, probes_loaded

        print(('loading script/instrument/probes config from {:s}'.format(file_name)))
        try:
            config = load_b26_file(file_name)['gui_settings']
            if config['settings_file'] != file_name:
                print((
                'WARNING path to settings file ({:s}) in config file is different from path of settings file ({:s})'.format(
                    config['settings_file'], file_name)))
            config['settings_file'] = file_name
            print(('loading of {:s} successful'.format(file_name)))
        except Exception:
            print(('WARNING path to settings file ({:s}) invalid use default settings'.format(file_name)))
            config = self._DEFAULT_CONFIG


            for x in list(self._DEFAULT_CONFIG.keys()):
                if x in config:
                    if not os.path.exists(config[x]):
                        try:
                            os.makedirs(config[x])
                        except Exception:
                            config[x] = self._DEFAULT_CONFIG[x]
                            os.makedirs(config[x])
                            print(('WARNING: failed validating or creating path: set to default path'.format(config[x])))
                else:
                    config[x] = self._DEFAULT_CONFIG[x]
                    os.makedirs(config[x])
                    print(('WARNING: path {:s} not specified set to default {:s}'.format(x, config[x])))

        # check if file_name is a valid filename
        if os.path.exists(os.path.dirname(file_name)):
            config['settings_file'] = file_name

        self.gui_settings = config

        self.instruments, self.scripts, self.probes = load_settings(file_name)


        self.refresh_tree(self.tree_gui_settings, self.gui_settings)
        self.refresh_tree(self.tree_scripts, self.scripts)
        self.refresh_tree(self.tree_settings, self.instruments)

        self._hide_parameters(file_name)


    def _hide_parameters(self, file_name):
        """
        hide the parameters that had been hidden
        Args:
            file_name: config file that has the information about which parameters are hidden

        """
        try:
            in_data = load_b26_file(file_name)
        except:
            in_data = {}

        def set_item_visible(item, is_visible):
            if isinstance(is_visible, dict):
                for child_id in range(item.childCount()):
                    child = item.child(child_id)
                    if child.name in is_visible:
                        set_item_visible(child, is_visible[child.name])
            else:
                item.visible = is_visible

        if "scripts_hidden_parameters" in in_data:
            # consistency check
            if len(list(in_data["scripts_hidden_parameters"].keys())) == self.tree_scripts.topLevelItemCount():

                for index in range(self.tree_scripts.topLevelItemCount()):
                    item = self.tree_scripts.topLevelItem(index)
                    # if item.name in in_data["scripts_hidden_parameters"]:
                    set_item_visible(item, in_data["scripts_hidden_parameters"][item.name])
            else:
                print('WARNING: settings for hiding parameters does\'t seem to match other settings')
        else:
            print('WARNING: no settings for hiding parameters all set to default')

    def save_config(self, out_file_name):
        """
        saves gui configuration to out_file_name
        Args:
            out_file_name: name of file
        """

        def get_hidden_parameter(item):

            numer_of_sub_elements = item.childCount()

            if numer_of_sub_elements == 0:
                dictator = {item.name : item.visible}
            else:
                dictator = {item.name:{}}
                for child_id in range(numer_of_sub_elements):
                    dictator[item.name].update(get_hidden_parameter(item.child(child_id)))
            return dictator

        out_file_name = str(out_file_name)
        if not os.path.exists(os.path.dirname(out_file_name)):
            os.makedirs(os.path.dirname(out_file_name))

        # build a dictionary for the configuration of the hidden parameters
        dictator = {}
        for index in range(self.tree_scripts.topLevelItemCount()):
            script_item = self.tree_scripts.topLevelItem(index)
            dictator.update(get_hidden_parameter(script_item))

        dictator = {"gui_settings": self.gui_settings, "scripts_hidden_parameters":dictator}

        # update the internal dictionaries from the trees in the gui
        for index in range(self.tree_scripts.topLevelItemCount()):
            script_item = self.tree_scripts.topLevelItem(index)
            self.update_script_from_item(script_item)

        dictator.update({'instruments': {}, 'scripts': {}, 'probes': {}})

        for instrument in self.instruments.values():
            dictator['instruments'].update(instrument.to_dict())
        for script in self.scripts.values():
            dictator['scripts'].update(script.to_dict())

        for instrument, probe_dict in self.probes.items():
            dictator['probes'].update({instrument: ','.join(list(probe_dict.keys()))})

        with open(out_file_name, 'w') as outfile:
            tmp = json.dump(dictator, outfile, indent=4)

    def save_dataset(self, out_file_name):
        """
        saves current dataset to out_file_name
        Args:
            out_file_name: name of file
        """

        for time_tag, script in self.data_sets.items():
            script.save(os.path.join(out_file_name, '{:s}.b26s'.format(time_tag)))


# In order to set the precision when editing floats, we need to override the default Editor widget that
# pops up over the text when you click. To do that, we create a custom Editor Factory so that the QTreeWidget
# uses the custom spinbox when editing floats
class CustomEditorFactory(QtWidgets.QItemEditorFactory):
    def createEditor(self, type, QWidget):
        if type == QtCore.QVariant.Double or type == QtCore.QVariant.Int:
            spin_box = QtWidgets.QLineEdit(QWidget)
            return spin_box

        if type == QtCore.QVariant.List or type == QtCore.QVariant.StringList:
            combo_box = QtWidgets.QComboBox(QWidget)
            combo_box.setFocusPolicy(QtCore.Qt.StrongFocus)
            return combo_box

        else:
            return super(CustomEditorFactory, self).createEditor(type, QWidget)

class MatplotlibWidget(Canvas):
    """
    MatplotlibWidget inherits PyQt4.QtWidgets.QWidget
    and matplotlib.backend_bases.FigureCanvasBase

    Options: option_name (default_value)
    -------
    parent (None): parent widget
    title (''): figure title
    xlabel (''): X-axis label
    ylabel (''): Y-axis label
    xlim (None): X-axis limits ([min, max])
    ylim (None): Y-axis limits ([min, max])
    xscale ('linear'): X-axis scale
    yscale ('linear'): Y-axis scale
    width (4): width in inches
    height (3): height in inches
    dpi (100): resolution in dpi
    hold (False): if False, figure will be cleared each time plot is called

    Widget attributes:
    -----------------
    figure: instance of matplotlib.figure.Figure
    axes: figure axes

    Example:
    -------
    self.widget = MatplotlibWidget(self, yscale='log', hold=True)
    from numpy import linspace
    x = linspace(-10, 10)
    self.widget.axes.plot(x, x**2)
    self.wdiget.axes.plot(x, x**3)
    """
    def __init__(self, parent=None):
        self.figure = Figure(dpi=100)
        Canvas.__init__(self, self.figure)
        self.axes = self.figure.add_subplot(111)

        self.canvas = self.figure.canvas
        self.setParent(parent)

        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def sizeHint(self):
        """
        gives qt a starting point for widget size during window resizing
        """
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        """
        minimum widget size during window resizing
        Returns: QSize object that specifies the size of widget
        """
        return QtCore.QSize(10, 10)
