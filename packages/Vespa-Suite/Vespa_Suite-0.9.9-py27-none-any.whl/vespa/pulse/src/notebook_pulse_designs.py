# Python modules
from __future__ import division
import os

# 3rd party modules
import wx
import wx.html
import wx.aui as aui

# Our modules
import tab_pulse_design
import vespa.common.util.misc as util_misc
import vespa.common.wx_gravy.common_dialogs as common_dialogs
import vespa.common.wx_gravy.notebooks as vespa_notebooks
import vespa.common.wx_gravy.util as wx_util


class NotebookPulseDesigns(vespa_notebooks.VespaAuiNotebook):
    """This is the main a.k.a. outer notebook containing all of the 
    pulse designs, each of which is iteself a notebook.
    """
    # I need the path to the welcome page image which is in vespa/common.
    _path = util_misc.get_vespa_install_directory()
    _path = os.path.join(_path, "common", "resources", "pulse_welcome.png")

    WELCOME_TAB_TEXT = """
    <html><body>
    <h1>Welcome to Vespa - Pulse</h1>
    <img src="%s" alt="Time-Freq Plots" />
    <p><b>Currently there are no pulse designs loaded.</b></p>
    <p>You can use the Pulse Design menu to load an existing pulse design or 
    create a new one.</p>
    </body></html>
    """ % _path
    # I tidy up my namespace by deleting this temporary variable.
    del _path

    def __init__(self, main_frame, db):
        vespa_notebooks.VespaAuiNotebook.__init__(self, main_frame)

        self._db = db
        self._main_frame = main_frame
        
        # Tracks the next number to be assigned to a pulse design tab.
        self._next_design_number = 1
        
        # I make my get_open_designs() method available to other parts
        # of the app.
        wx.GetApp().vespa.get_open_designs = self.get_open_designs
        
        self.show_welcome_tab()

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_page_close)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.on_page_closed)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        
        
    #=======================================================
    #
    #           Event handlers start here 
    #                 (alphabetized)
    #
    #=======================================================
    def on_menu_view_option(self, event):
        if self.active_tab: 
            self.active_tab.on_menu_view_option(event)


    def on_menu_view_output(self, event):
        if self.active_tab:
            self.active_tab.on_menu_view_output(event)


    def on_page_changed(self, event):
        name = ""
        
        # Create an appropriate name from whatever page/tab is selected.
        if self.active_tab:
            name = self.active_tab.pulse_design.name
            
            if name:
                states = [ ]
                if self.active_tab.pulse_design.is_frozen:
                    states.append("frozen")
                if self.active_tab.pulse_design.referrers:
                    states.append("in use")
                if self.active_tab.pulse_design.is_public:
                    states.append("public")
                states = ", ".join(states)
                if states:
                    states = " (" + states + ")"
                    
                name += states
            else:
                name = "New Pulse Design"
                
            name = " - " + name
                
            self.active_tab.on_activation()

        self._main_frame.SetTitle("Pulse" + name)
        # Clear the status bar
        statusbar = wx.GetApp().vespa.statusbar
        for i in range(statusbar.GetFieldsCount()):
            statusbar.SetStatusText("", i)


    def on_page_close(self, event):
        veto = False
        if self.active_tab:
            veto = not self.active_tab.close()
        else:
            # The active tab is the welcome tab; we ignore the close request.
            veto = True
        
        if veto:
            event.Veto()


    def on_page_closed(self, event):
        if not self.GetPageCount():
            self.show_welcome_tab()


    #=======================================================
    #
    #     Internal & shared helper methods start here 
    #                 (alphabetized)
    #
    #=======================================================


    def add_transform(self, kernel):
        if self.active_tab:
            self.active_tab.add_transform(kernel)
    
    
    def add_pulse_design_tab(self, pulse_design=None):
        # Delete the welcome page if it's open.
        if self.is_welcome_tab_open:
            self.DeletePage(0)
        
        # Create new notebook with pulse design controls and display        
        tab = tab_pulse_design.TabPulseDesign(self._main_frame, self._db, pulse_design)

        # Add the tab. Note that this tab will contain yet another notebook.
        title = "Pulse Design %d" % self._next_design_number
        self._next_design_number += 1
        self.AddPage(tab, title, True)


    def close_all(self):
        """
        Attemps to close all open designs. If a tab contains 
        unsaved changes, the user will be prompted and can cancel the close.
        
        Returns True if all tabs were closed or False if any were cancelled.
        """
        close_accepted = True
        # While there are tabs open and the user hasn't cancelled,
        # close the current tab.
        i = len(self.tabs)
        while i and close_accepted:
            self.close_pulse_design()
            # There should be one less tab now. If not, the user cancelled 
            # the close.
            i -= 1
            close_accepted = (i == len(self.tabs))
            
        return close_accepted


    def close_pulse_design(self):
        if self.active_tab:
            wx_util.send_close_to_active_tab(self)


    def copy_tab(self):
        if self.active_tab:
            msg = "The copy will be made from the last time this " \
                  "pulse design was saved or run."
            common_dialogs.message(msg, "Copy Tab to New Pulse Design", 
                                   common_dialogs.I_OK)
            
            pulse_design = self.active_tab.pulse_design.clone()
            pulse_design.id = util_misc.uuid()
            # Add "copy" to the name. This is just a convenience for the 
            # user so that when they save a copied tab we usually won't have
            # to bug them to change the name first. It's not guaranteed to be
            # unique, but it will be most of the time and that's good enough.
            pulse_design.name += " copy"
            
            self.add_pulse_design_tab(pulse_design)

        
    def get_open_designs(self):
        """
        Returns a (possibly empty) list of the pulse designs currently 
        open in tabs.
        """
        return [tab.pulse_design for tab in self.tabs]


    def save_pulse_design(self):
        if self.active_tab:
            self.active_tab.save()


    def save_as_pulse_design(self):
        if self.active_tab:
            self.active_tab.save(True)
