# -*- coding: utf-8 -*-

'''
GUI operations in EMBL2checklists
'''

#####################
# IMPORT OPERATIONS #
#####################
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'EMBL2checklists'))

import Tkinter as tk
import tkFileDialog
from tkFileDialog import askopenfilename, asksaveasfilename

import EMBL2checklistsMain as E2C
import globalVariables as GlobVars

###############
# AUTHOR INFO #
###############
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>,\
              Yannick Hartmaring <yanjo@zedat.fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2018 Michael Gruenstaeudl'
__info__ = 'EMBL2checklists'
__version__ = '2018.11.30.1800'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

#############
# VARIABLES #
#############
generalBG = "#93BDAC"
buttonBG = "white"
entryBG = "white"
generalFG = "black"
buttonFG = "black"
entryFG = "black"

###########
# CLASSES #
###########

class GUI():

########################################################################

    def __init__(self):

    ## WINDOW ##
        self.window = tk.Tk()
        self.window.title("EMBL2checklists")
        self.window.geometry("460x400")
        self.window.configure(background=generalBG)

    ## VARIABLES ##
        self.outFile = tk.StringVar()
        self.inFile = tk.StringVar()
        self.outFile.set("")
        self.isEnv = 'no'
        self.inFile.set("")
        self.data = GlobVars.implemented_checklists

        self.checklistHelper = {'ITS':'For ITS rDNA region. This checklist'
                                      + ' allows generic annotation of the ITS'
                                      + ' components (18S rRNA, ITS1, 5.8S rRNA,'
                                      + ' ITS2 and 28S rRNA). For annotation of'
                                      + ' the rRNA component only, please use'
                                      + ' the rRNA gene checklist.',
                                'IGS':'For intergenic spacer (IGS) sequences'
                                      + ' between neighbouring genes (e.g.,'
                                      + ' psbA-trnH IGS, 16S-23S rRNA IGS).'
                                      + ' Inclusion of the flanking genes is'
                                      + ' allowed.',
                          'trnK_matK':'For complete or partial matK gene within'
                                      + ' the chloroplast trnK gene intron.',
                                'ETS':'For submission of External Transcribed'
                                      + ' Spacer (ETS) regions of the'
                                      + ' eukaryotic rDNA transcript; a region'
                                      + ' often used to study intrageneric'
                                      + ' relationships.',
                               'rRNA':'For ribosomal RNA genes from'
                                      + ' prokaryotic, nuclear or organellar'
                                      + ' DNA. All rRNAs are considered'
                                      + ' partial.',
                        'gene_intron':'For complete or partial single gene'
                                      + ' intron.'
                                    }

        self.clType = tk.StringVar()
        self.clType.set('ITS')
        self.checklistLabel = tk.Message(text=self.checklistHelper[self.clType.get()], width=320, background=generalBG, foreground=generalFG, anchor="nw", bd=2)
        self.clType.trace("w",self.callback)

        self.gui()

########################################################################

    def gui(self):

    ## LABEL ##
        chooseEMBL = tk.Label(text="Input:", background=generalBG, foreground=generalFG)
        chooseOutput = tk.Label(text="Output:", background=generalBG, foreground=generalFG)
        chooseCLType = tk.Label(text="Checklist Type:", background=generalBG, foreground=generalFG)
        isEnv = tk.Message(text="Is your organism from an environmental/uncultured sample?", background=generalBG, foreground=generalFG, anchor="nw", width=300)
        self.helperLabel = tk.Message(master=self.window, text="", width=240, background=generalBG, foreground=generalFG)

    ## BUTTON ##
        submitButton = tk.Button(master=self.window, text="Submit", command=self.submit, background=buttonBG, foreground=buttonFG)
        chooseFileButton = tk.Button(master=self.window, text="Choose File", command=self.chooseFile, background=buttonBG, foreground=buttonFG)
        chooseOutFileButton = tk.Button(master=self.window, text="Choose File", command=self.saveFile, background=buttonBG, foreground=buttonFG)
        closeButton = tk.Button(master=self.window, text="Close", command=self.window.quit, background=buttonBG, foreground=buttonFG)

        self.yesCheckbutton = tk.Checkbutton(master=self.window, text="yes", background=buttonBG, command=self.isEnvTrue)
        self.noCheckbutton = tk.Checkbutton(master=self.window, text="no", background=buttonBG, command=self.isEnvFalse)
        self.noCheckbutton.select()

    ## ENTRY ##
        outputEntry = tk.Entry(master=self.window, textvariable=self.outFile, background=entryBG, foreground=entryFG)
        inputEntry = tk.Entry(master=self.window, textvariable=self.inFile, background=entryBG, foreground=entryFG)

    ## DROPDOWN ##
        dropdown = tk.OptionMenu(self.window, self.clType, *self.data)

    ## PRINTER ##
        chooseEMBL.place(x=10,y=10, width=110, height=40)
        inputEntry.place(x=130,y=10, width=210, height=40)
        chooseFileButton.place(x=350,y=10, width=100, height=40)

        chooseOutput.place(x=10,y=70, width=110, height=40)
        outputEntry.place(x=130,y=70, width=210, height=40)
        chooseOutFileButton.place(x=350,y=70, width=100, height=40)

        chooseCLType.place(x=10,y=130, width=110, height=40)
        dropdown.place(x=130,y=130, width=210, height=40)

        self.checklistLabel.place(x=130,y=170, width=320, height=200)

        isEnv.place(x=10,y=280,width=300,height=40)
        self.yesCheckbutton.place(x=270,y=290)
        self.noCheckbutton.place(x=330,y=290)

        closeButton.place(x=10,y=350, width=100, height=40)
        submitButton.place(x=350,y=350, width=100, height=40)
        self.helperLabel.place(x=110,y=340, width=240, height=50)

        submitButton.bind("<Enter>", self.on_enterSubmitButton)
        submitButton.bind("<Leave>", self.on_leave)

        chooseFileButton.bind("<Enter>", self.on_enterInput)
        chooseFileButton.bind("<Leave>", self.on_leave)

        chooseOutFileButton.bind("<Enter>", self.on_enterOutput)
        chooseOutFileButton.bind("<Leave>", self.on_leave)

        dropdown.bind("<Enter>", self.on_enterChecklisttype)
        dropdown.bind("<Leave>", self.on_leave)

        self.yesCheckbutton.bind("<Enter>", self.on_enterEnvSample)
        self.yesCheckbutton.bind("<Leave>", self.on_leave)

        self.noCheckbutton.bind("<Enter>", self.on_enterEnvSample)
        self.noCheckbutton.bind("<Leave>", self.on_leave)

        closeButton.bind("<Enter>", self.on_enterClose)
        closeButton.bind("<Leave>", self.on_leave)

    ## MAINLOOP ##
        self.window.mainloop()

########################################################################

    ## FUNCTIONS ##
    def submit(self):
        GlobVars.warnings = []
        try:
            if self.clType.get() in GlobVars.implemented_checklists:
                if self.inFile.get().split('.')[-1] == 'embl':
                    E2C.EMBL2checklists(self.inFile.get(), self.outFile.get(), 'embl', self.clType.get(), self.isEnv)
                    self.ready()
                elif self.inFile.get().split('.')[-1] == 'gb':
                    E2C.EMBL2checklists(self.inFile.get(), self.outFile.get(), 'gb', self.clType.get(), self.isEnv)
                    self.ready()
                else:
                    raise Exception('The file ending of ´%s´ does not match any of the permissible flatfile formats (.embl, .gb).' % (self.inFile.get()))
            else:
                raise Exception('ERROR: The selection ´%s´ is not an implemented checklist type.' % (self.clType.get()))
        except Exception as e:
            try:
                self.errorMessage(e)
            except:
                print e

########################################################################

    def ready(self):
        if len(GlobVars.warnings) != 0:
            self.warningMessage(GlobVars.warnings)
        self.doneMessage()

    def callback(self,*args):
        self.checklistLabel.configure(text=self.checklistHelper[self.clType.get()])

    def isEnvTrue(self):
        if self.isEnv == 'no':
            self.noCheckbutton.deselect()
            self.isEnv = 'yes'
        else:
            self.yesCheckbutton.select()

    def isEnvFalse(self):
        if self.isEnv == 'yes':
            self.yesCheckbutton.deselect()
            self.isEnv = 'no'
        else:
            self.noCheckbutton.select()

    def on_enterSubmitButton(self, event):
        self.helperLabel.configure(text="Click to start the program")

    def on_enterInput(self, event):
        self.helperLabel.configure(text="Click to choose an input file in GenBank or EMBL flatfile format")

    def on_enterOutput(self, event):
        self.helperLabel.configure(text="Click to set name and path of the output file")

    def on_enterChecklisttype(self, event):
        self.helperLabel.configure(text="Choose the appropriate checklist type")

    def on_enterEnvSample(self, event):
        self.helperLabel.configure(text="Is your organism from an environmental/uncultured sample? (yes/no)")

    def on_enterClose(self, event):
        self.helperLabel.configure(text="Click to close the program")

    def on_leave(self, enter):
        self.helperLabel.configure(text="")

    def chooseFile(self):
        fileChooser = tk.Tk()
        fileChooser.withdraw()
        filename = askopenfilename()
        fileChooser.destroy()
        self.inFile.set(filename)
        self.outFile.set(filename.split("/")[-1].split(".")[0] + ".tsv")

    def saveFile(self):
        fileChooser = tk.Tk()
        fileChooser.withdraw()
        filename = asksaveasfilename(initialdir=".", title="Select file", filetypes=(("LibreOffice",".tsv"),("ENA Webin checklist","*.checklist"),("all files","*.*")))
        fileChooser.destroy()
        self.outFile.set(filename)

########################################################################

    ## ERROR WINDOW ##
    def errorMessage(self, error):
        errorWindow = tk.Tk()
        errorWindow.title("Error " + error.getErrorNumber() + ": " + error.getErrorName())
        errorWindow.geometry("420x100")
        errorWindow.configure(background=generalBG)

        #Label
        errorMessage= tk.Message(master=errorWindow, text=error.value, width='400')
        errorMessage.place(x=10,y=10, width=400, height=40)

        #Button
        errorWindow = tk.Button(master=errorWindow, text="OK", command=errorWindow.destroy)
        errorWindow.place(x=160, y=50, width=110, height=40)

########################################################################

    ## WARNING WINDOW ##
    def warningMessage(self, warningList):
        ErrorMsgHeight = 75
        ErrorSpacing = 10
        ButtonHeight = 40
        warningWindow = tk.Tk()
        warningWindow.title("Warnings")
        height = (10+len(warningList)*ErrorMsgHeight)+ButtonHeight+(ErrorSpacing*3)
        warningWindow.geometry("520x" + str(height))
        warningWindow.configure(background=generalBG)

        warningString = ''
        for counter, warning in enumerate(warningList):

            #Label
            warningLabel = tk.Label(master=warningWindow, text=warning, background=generalBG, foreground=generalFG)
            warningLabel.place(x=10, y=10+counter*ErrorMsgHeight, width=500, height=ErrorMsgHeight+ErrorSpacing)
            #warningLabel.place(x=10, y=10, width=500, height=100)

        #Button
        warningButton = tk.Button(master=warningWindow, text="OK", command=warningWindow.destroy, background=buttonBG, foreground=buttonFG)
        warningButton.place(x=190, y=(10+len(warningList)*ErrorMsgHeight)+(ErrorSpacing*2), width=150, height=ButtonHeight)

########################################################################

    ## DONE WINDOW ##
    def doneMessage(self):
        doneWindow = tk.Tk()
        doneWindow.title("EMBL2checklists")
        doneWindow.geometry("420x130")
        doneWindow.configure(background=generalBG)

        #Label
        doneLabel = tk.Label(master=doneWindow, text="PROCESS COMPLETE.\nOutput location: " + self.outFile.get(), background=generalBG, foreground=generalFG, wraplength=390)
        doneLabel.place(x=10, y=10, width=400, height=60)

        #Button
        doneButton = tk.Button(master=doneWindow, text="Done", command=doneWindow.destroy, background=buttonBG, foreground=buttonFG)
        doneButton.place(x=160, y=80, width=110, height=40)

########################################################################


########
# MAIN #
########

def start_EMBL2checklists_GUI():
    GUI()
