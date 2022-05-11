#Vertical Scrolled Frame class was created by github user @novel-yet-trivial
#Input directory was used from Stack Overflow user @scotty3785
#All other code written by William Mears III
#-------------------------------------------------------------------------------------------------------------------------------------
#Import neccessary packages
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import tkinter.messagebox
import pandas as pd
import tkinter as tk
import numpy as np
import os
import csv
#-------------------------------------------------------------------------------------------------------------------------------------
#Define entire code as a function, neccessary for turning into EXE
#CMD prompt to make executable : pyinstaller.exe --onefile --noconsole --icon=logoFITSSTATS.ico fitsimagestats2.py 
def main():
    #---------------------------------------------------------------------------------------------------------------------------------
    #Portion to initialize and name window
    window = Tk()
    window.geometry('1345x490') #Set window parameters
    window.title("FITS Image Stats 2.0") #name window
    #os.chdir(os.getcwd())
    #window.iconbitmap(logoFITSSTATS.ico)#set icon for program
    #---------------------------------------------------------------------------------------------------------------------------------
    #Vertical Scrolled Frame class, created by github user @novel-yet-trivial    
    class VerticalScrolledFrame:
        def __init__(self, master, **kwargs):
            width = kwargs.pop('width', None)
            height = kwargs.pop('height', None)
            bg = kwargs.pop('bg', kwargs.pop('background', None))
            self.outer = tk.Frame(master, **kwargs)
            self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
            self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
            self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.canvas['yscrollcommand'] = self.vsb.set
            self.canvas.bind("<Enter>", self._bind_mouse)
            self.canvas.bind("<Leave>", self._unbind_mouse)
            self.vsb['command'] = self.canvas.yview
            self.inner = tk.Frame(self.canvas, bg=bg)
            self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
            self.inner.bind("<Configure>", self._on_frame_configure)
            self.outer_attr = set(dir(tk.Widget))
        def __getattr__(self, item):
            if item in self.outer_attr:
                return getattr(self.outer, item)
            else:
                return getattr(self.inner, item)
        def _on_frame_configure(self, event=None):
            x1, y1, x2, y2 = self.canvas.bbox("all")
            height = self.canvas.winfo_height()
            self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))
        def _bind_mouse(self, event=None):
            self.canvas.bind_all("<4>", self._on_mousewheel)
            self.canvas.bind_all("<5>", self._on_mousewheel)
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        def _unbind_mouse(self, event=None):
            self.canvas.unbind_all("<4>")
            self.canvas.unbind_all("<5>")
            self.canvas.unbind_all("<MouseWheel>")
        def _on_mousewheel(self, event):
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units" )
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units" )
        def __str__(self):
            return str(self.outer)
    #---------------------------------------------------------------------------------------------------------------------------------
    #Portion to initially place canvas on grid. This canvas will be destroyed and written over whenever the clear button is selected
    #Canvas is defined globally so it can be destroyed in the clear function
    global canv
    canv = VerticalScrolledFrame(window, width=1000, borderwidth=2, relief=tk.SUNKEN, background="light gray")
    canv.grid(column=0, row=11)
    #---------------------------------------------------------------------------------------------------------------------------------
    #Input directory, created by Stack Overflow user scotty3785
    class FolderSelect(Frame):
        def __init__(self,parent=None,folderDescription="",**kw):
            Frame.__init__(self,master=parent,**kw)
            self.folderPath = StringVar()
            self.lblName = Label(self, text=folderDescription, font=("Arial Bold", 10))
            self.lblName.grid(row=1,column=0)
            self.entPath = Entry(self, textvariable=self.folderPath)
            self.entPath.grid(row=1,column=1)
            self.btnFind = ttk.Button(self, text="Browse Folder",command=self.setFolderPath)
            self.btnFind.grid(row=1,column=2)
        def setFolderPath(self):
            folder_selected = filedialog.askdirectory()
            self.folderPath.set(folder_selected)
        @property
        def folder_path(self):
            return self.folderPath.get()
    folderPath = StringVar()
    #---------------------------------------------------------------------------------------------------------------------------------
    #Section initializes all labels, entry boxes, check buttons, and directory select buttons
    lbl = Label(window, text="FITS Image Stats 2.0", font=("Arial Bold", 10)) #Set label for title
    lbl.grid(column=0, row=0)  #place title on grid
    lbl = Label(window, text="Note: If program says 'Not Responding', allow it to continue running, it eventually will work.", font=("Arial", 10)) #Set label for note
    lbl.grid(column=0, row=1)  #place note on grid
    directory1Select = FolderSelect(window,"Choose folder to get FITS image stats from ") #Directory select function called for first directory
    directory1Select.grid(row=2) #Place directory select on row
    lblTwo = Label(window, 
    text="Choose from full frame, default sub (1k x 1k, starting from (150,150)), or choose Chosen Subframe (starting from (150,150)) to input your own dimensions.", 
    font=("Arial Bold", 10)) #Set label for frame options
    lblTwo.grid(column=0, row=3) #place label on grid
    chk_state = BooleanVar()#Make check state true or false variable
    chk_state.set(False) #Have check box set to false upon opening window
    chk_stateOne = BooleanVar()#^
    chk_stateOne.set(False)#^
    chk_stateTwo = BooleanVar()#^
    chk_stateTwo.set(False)#^
    chk = Checkbutton(window, text='Full Frame', var=chk_state) #Set Full Frame check box and assign to boolean variable
    chk.grid(column=1, row=3)#Place check box on grid
    chkOne = Checkbutton(window, text='Default Subframe', var=chk_stateOne) #Set Default Frame check box and assign to boolean variable
    chkOne.grid(column=2, row=3)#Place check box on grid
    chkTwo = Checkbutton(window, text='Chosen Subframe', var=chk_stateTwo) #Set Chosen Frame check box and assign to boolean variable
    chkTwo.grid(column=3, row=3)#Place check box on grid
    yLabel = Label(window, text="If 'Chosen Subframe', enter y axis dimensions", font=("Arial Bold", 10)) #If subframe, y label for parameters
    yLabel.grid(column=0, row=4) #Place label on grid
    yEntry = Entry(window,width=10) #If subframe, y entry for parameters
    yEntry.grid(column=1, row=4)#Place entry on grid
    xLabel = Label(window, text="If 'Chosen Subframe', enter x axis dimensions", font=("Arial Bold", 10)) #If subframe, x label for parameters
    xLabel.grid(column=0, row=5) #Place label on grid
    xEntry = Entry(window,width=10) #If subframe, x entry for parameters
    xEntry.grid(column=1, row=5)#Place entry on grid
    lab = Label(window, text="Would you like to display the information on screen and/or write to csv file?", font=("Arial Bold", 10)) #Label for write or display
    lab.grid(column=0, row=6) #place label on grid
    check_state = BooleanVar()#Make check state true or false variable
    check_state.set(False)#Have check box set to false upon opening window
    check_stateOne = BooleanVar()#^
    check_stateOne.set(False)#^
    check = Checkbutton(window, text='Write', var=check_state) #Set write check box and assign to boolean variable
    check.grid(column=1, row=6)#Place on grid
    checkOne = Checkbutton(window, text='Display', var=check_stateOne) #Set display check box and assign to boolean variable
    checkOne.grid(column=2, row=6) #Place on grid
    lblTwo = Label(window, text="If write, what would you like to name your csv file? (format : example.csv)", font=("Arial Bold", 10)) #Label for csv file name
    lblTwo.grid(column=0, row=7)#Place on grid
    txtThree = Entry(window,width=10)#Entry for naming csv file
    txtThree.grid(column=1, row=7)#Place on grid
    directory2Select = FolderSelect(window,"If write, choose location to save csv ")#Directory select function for choosing location to save csv file
    directory2Select.grid(row=8)#Place on grid
    #---------------------------------------------------------------------------------------------------------------------------------
    #Set a variable
    #Set a as global so it can be used in process and clear with value set to one upon running the program. After initially running the program,
    #these two lines will not be ran through again. This variable is for placing labels on canvas. Every time a label is placed, a increases. 
    #If the clear button is selected, a is set back to one so, when the process button is pressed again, a will start by placing label on first row in canvas
    global a 
    a = 1 #a set to one outside of process function
    #---------------------------------------------------------------------------------------------------------------------------------
    #Process function for all reasonable actions desired by user
    def process():
        global a #Call a global again so function recognizes count when called upon
        #Error Handling
        if directory1Select.folder_path == '': #Error if no directory
            tk.messagebox.showinfo("Error", "Enter a directory") #Show message box
            return #Exit function
        if str(yEntry.get()) == '' and chk_stateTwo.get() == True: #Error if y entry is empty and chosen subframe is true
            tk.messagebox.showinfo("Error", "Enter y dimension for chosen subframe")#Show message box
            return #Exit function
        if str(xEntry.get()) == '' and chk_stateTwo.get() == True: #Error if y entry is empty and chosen subframe is true
            tk.messagebox.showinfo("Error", "Enter x dimension for chosen subframe")#Show message box
            return#Exit function
        if chk_stateTwo.get() == False and chk_stateOne.get() == False and chk_state.get() == False: #Error if no frame type is selected
            tk.messagebox.showinfo("Error", "Enter Frame type")#show messagebox
            return#Exit function
        if check_state.get() == False and check_stateOne.get() == False : #Error if no output type is selected
            tk.messagebox.showinfo("Error", "Choose either write or display")#show messagebox
            return#Exit function
        if str(txtThree.get()) == '' and check_state.get() == True : #Error if write selected and no csv file named
            tk.messagebox.showinfo("Error", "Enter name to save csv file")#show messagebox
            return#Exit function
        if '.csv' not in str(txtThree.get()) and check_state.get() == True : #Error if write selected and no csv file name in improper format
           tk.messagebox.showinfo("Error", "Please format csv file as follows : example.csv")#show messagebox
           return #Exit function
        if directory2Select.folder_path == '' and check_state.get() == True : #Error if write selected and no csv save location selected
            tk.messagebox.showinfo("Error", "Enter directory to save csv file")#show messagebox
            return#Exit function
        try:
            if chk_stateTwo.get() == True : #See if turning entries into an integer produces an error
                int(xEntry.get())
                int(yEntry.get())
        except:#If it does, show messagebox and kill function
            tk.messagebox.showinfo("Error" , "Enter proper x and y coordinates (integer)")
            return
        #-----------------------------------------------------------------------------------------------------------------------------
        #The only time that there will be a widget in row 10 is after the code has been cleared or process has been ran
        #Row 10 is for displaying messages that confirm the action desired has been completed. For example, if row 10 says "All values 
        #cleared successfuly", at this point in the process function that will be cleared, so another label, like "values
        #successfuly displayed" can be placed in row 10
        for displ in window.grid_slaves():
            if int(displ.grid_info()["row"]) == 10:
                 displ.grid_forget()
        #-----------------------------------------------------------------------------------------------------------------------------
        #Get values from all entries. If the values are not needed, ie. n or m when the user doesn't select Chosen Subframe,
        #the value will simply not be used
        directory = directory1Select.folder_path #set directory as entry input
        directory2 = directory2Select.folder_path #directory for writing to csv
        err = 0 #Variable created to notify user if there are no FTS files in entered directory, explained further when called upon
        u = 0 #Variable for exiting function from for loop
        #-----------------------------------------------------------------------------------------------------------------------------
        #All values that are entered to csv file are put into a data frame, which is INITIALIZED here. Data frame has axis titles
        #to keep all data in order, but the actual titles displayed in the csv file are placed in the first row of the dataframe.
        #This was done because dataframes are formatted in a way that both row and column axes have titles. Although it's
        #possible to just title the column axis as Object and have each row axis be the filename, this causes (1,1) in the csv file to
        #be an empty cell    
        csvDf = pd.DataFrame({'File Name' : [], 'Average': [], 'STD': [], 'Median': [], 'Frame Type': []}) #create DF for writing to csv
        frame = pd.DataFrame({'File Name' : ['Filename'], 'Average': ['Average'], 'STD': ['STD'], 'Median': ['Median'], 'Frame Type': ['Frame Type']}) #enter dataframe titles
        csvDf = [csvDf, frame] #enter structure for concatenation
        csvDf = pd.concat(csvDf) #concatenate the data set and titles
        #-----------------------------------------------------------------------------------------------------------------------------
        #Set title for display before for loop, so the title doesn't get added onto the display each iteration
        if check_stateOne.get() == True: #if display is checked
            l = Label(canv, text="Filename", font=("Arial Bold", 10)) #Set filename title
            l.grid(column=0, row=0) #Place on grid
            lOne = Label(canv, text="Average in ADU/pix", font=("Arial Bold", 10)) #Set Average title
            lOne.grid(column=1, row=0)  #Place on grid
            lTwo = Label(canv, text="STD", font=("Arial Bold", 10)) #Set STD title
            lTwo.grid(column=2, row=0)  #Place on grid
            lThree = Label(canv, text="Median", font=("Arial Bold", 10)) #Set Median title
            lThree.grid(column=3, row=0)  #Place on grid       
            lFour = Label(canv, text="Frame Type", font=("Arial Bold", 10)) #Set Frame type title
            lFour.grid(column=4, row=0)#Place on grid
        #-----------------------------------------------------------------------------------------------------------------------------
        #For loop that iterates through each file and completes neccesary action
        if chk_stateTwo.get() == True: #if chosen sub frame selected, convert entries to int and use as parameters
            n = int(yEntry.get()) #Get vertical dimension
            m = int(xEntry.get()) #Get horizontal dimension
        for filename in os.listdir(directory): #Iterate through directory
            if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"): #Only go through FTS files
                err = err + 1 #Add one to err for each FTS file, though after adding to err once the value is trivial 
                #---------------------------------------------------------------------------------------------------------------------
                #if full frame selected
                if chk_state.get() == True: #If full frame box checked
                    x = fits.open(os.path.join(directory, filename)) #Open fits file
                    x = x[0].data #retrieve fits file data
                    x = np.matrix(x) #convert data to np matrix
                    #---------------------------------------------------------------------------------------------------------------------
                    #If write selected
                    #The codes for both write and display are each used three times : Under each possible frame type. This is done, as 
                    #opposed to only writing write and display below all of the frame if statements, in case the user chooses more than
                    #one frame type. If they were only put once each at the end of the for loop, the matrix would only display
                    #the bottom most frame type in the for loop. Write and display could easily be turned into functions, with
                    #row being one parameter and frame type being another, but it doesn't make a difference
                    if check_state.get() == True: 
                        frame = pd.DataFrame({'File Name' : [filename], 'Average': [str('{:.1f}'.format(round(np.matrix.mean(x), 1)))], 
                        'STD': [str('{:.1f}'.format(round(np.matrix.std(x), 1)))], 
                        'Median': [str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1)))], 'Frame Type': ['Full']}) #Add each datapoint to set
                        csvDf = [csvDf, frame] #create structure for concatenation
                        csvDf = pd.concat(csvDf) #Concatenate
                    #---------------------------------------------------------------------------------------------------------------------
                    #If display selected, add each label on grid in appropriate position
                    if check_stateOne.get() == True:
                        l = Label(canv, text= str(filename), font=("Arial Bold", 10))
                        l.grid(column=0, row=a) 
                        lOne = Label(canv, text=str('{:.1f}'.format(round(np.matrix.mean(x), 1))), font=("Arial Bold", 10))
                        lOne.grid(column=1, row=a) 
                        lTwo = Label(canv, text=str('{:.1f}'.format(round(np.matrix.std(x), 1))), font=("Arial Bold", 10))
                        lTwo.grid(column=2, row=a) 
                        lThree = Label(canv, text=str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1))), font=("Arial Bold", 10))
                        lThree.grid(column=3, row=a)
                        lFour = Label(canv, text='Full', font=("Arial Bold", 10))
                        lFour.grid(column=4, row=a)
                        a = a + 1                      
                #---------------------------------------------------------------------------------------------------------------------
                #if default frame selected                                
                if chk_stateOne.get() == True:
                    x = fits.open(os.path.join(directory, filename)) #Open fits file
                    x = x[0].data #get data from file
                    x = np.matrix(x) #Convert data to matrix
                    x = x[150:1150,150:1150] #slice matrix to be 1k by 1k starting from (150,150)
                    #-----------------------------------------------------------------------------------------------------------------
                    #If write selected                           
                    if check_state.get() == True: 
                        frame = pd.DataFrame({'File Name' : [filename], 'Average': [str('{:.1f}'.format(round(np.matrix.mean(x), 1)))], 
                        'STD': [str('{:.1f}'.format(round(np.matrix.std(x), 1)))], 
                        'Median': [str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1)))], 'Frame Type': ['Default']})
                        csvDf = [csvDf, frame]
                        csvDf = pd.concat(csvDf)
                    #-----------------------------------------------------------------------------------------------------------------
                    #If display selected  
                    if check_stateOne.get() == True:
                        l = Label(canv, text= str(filename), font=("Arial Bold", 10))
                        l.grid(column=0, row=a) 
                        lOne = Label(canv, text=str('{:.1f}'.format(round(np.matrix.mean(x), 1))), font=("Arial Bold", 10))
                        lOne.grid(column=1, row=a) 
                        lTwo = Label(canv, text=str('{:.1f}'.format(round(np.matrix.std(x), 1))), font=("Arial Bold", 10))
                        lTwo.grid(column=2, row=a) 
                        lThree = Label(canv, text=str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1))), font=("Arial Bold", 10))
                        lThree.grid(column=3, row=a)                       
                        lFour = Label(canv, text='Default', font=("Arial Bold", 10))
                        lFour.grid(column=4, row=a)
                        a = a + 1                      
                #---------------------------------------------------------------------------------------------------------------------
                #if chosen frame selected                      
                if chk_stateTwo.get() == True: #if chosen sub frame selected, convert entries to int and use as parameters
                    x = fits.open(os.path.join(directory, filename)) #open fts file
                    x = x[0].data
                    x = np.matrix(x)
                    x = x[150:150+n,150:150+m] #slice np matrix to be n x m starting at 150,150
                #---------------------------------------------------------------------------------------------------------------------
                #More error handling : this has to do with the dimensions inputed for chose subframe. If the dimensions are larger than
                #the frame, the user is asked if they'd like to continue with the largest available frame. If yes, the code changes the 
                #dimension to be the largest available, and consequently won't run through the if statement again
                    if (len(x)) < n : #If vertical dimension is too large
                        tk.messagebox.showinfo("Error", "Vertical dimension larger than maximum while starting at (150px,150px)")
                        askTwo = tk.messagebox.askquestion("Error", "Would you like to continue with largest allowable vertical dimension? (" + str(len(x)) + "px)")
                        if askTwo == 'no': #if user doesn't want to continue, set u to 1 so function can be killed
                            u = 1
                            return
                        else : #If user wants to continue parsing, change length to max allowable
                            n = len(x)
                    if (len(x)) < m : #If horizontal dimension is too large
                        tk.messagebox.showinfo("Error", "Horizontal dimension larger than maximum while starting at (150px,150px)")
                        askThree = tk.messagebox.askquestion("Error", "Would you like to continue with largest allowable horizontal dimension? (" + str(len(x)) + "px)")
                        if askThree == 'no': #if user doesn't want to continue, set u to 1 so function can be killed
                            u = 1
                            return
                        else : #If user wants to continue parsing, change length to max allowable
                            m = len(x)
                    #---------------------------------------------------------------------------------------------------------------------
                    #If write selected                           
                    if check_state.get() == True: 
                        frame = pd.DataFrame({'File Name' : [filename], 'Average': [str('{:.1f}'.format(round(np.matrix.mean(x), 1)))],
                        'STD': [str('{:.1f}'.format(round(np.matrix.std(x), 1)))], 
                        'Median': [str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1)))], 'Frame Type': [str(n) + 'x' + str(m) + ' Subframe']})
                        csvDf = [csvDf, frame]
                        csvDf = pd.concat(csvDf)
                    #---------------------------------------------------------------------------------------------------------------------
                    #If display selected  
                    if check_stateOne.get() == True:
                        l = Label(canv, text= str(filename), font=("Arial Bold", 10))
                        l.grid(column=0, row=a) 
                        lOne = Label(canv, text=str('{:.1f}'.format(round(np.matrix.mean(x), 1))), font=("Arial Bold", 10))
                        lOne.grid(column=1, row=a) 
                        lTwo = Label(canv, text=str('{:.1f}'.format(round(np.matrix.std(x), 1))), font=("Arial Bold", 10))
                        lTwo.grid(column=2, row=a) 
                        lThree = Label(canv, text=str('{:.1f}'.format(round(np.median(np.squeeze(np.asarray(x))), 1))), font=("Arial Bold", 10))
                        lThree.grid(column=3, row=a)
                        lFour = Label(canv, text=str(n) + 'x' + str(m) + ' Subframe', font=("Arial Bold", 10))
                        lFour.grid(column=4, row=a)                        
                        a = a + 1  
            else:
                continue
        #-----------------------------------------------------------------------------------------------------------------------------
        #Variables for exiting out of function        
        if u == 1 : #u will only be 1 if the user chooses to not continue parsing after entering a dimension that is too large
            return
        if err == 0 : #If directory doesn't contain any FTS files, kill function
            tk.messagebox.showinfo("Error", "Directory doesn't contain FTS files")
            return
        #-----------------------------------------------------------------------------------------------------------------------------
        #Write to csv, display different variation of success in row 10        
        if check_state.get() == True and  check_stateOne.get() == False: #If write selected
            csvDf.to_csv(os.path.join(directory2, str(txtThree.get())), header=None, index=None)
            labe = Label(window, text="Successfully saved csv file in location", font=("Arial Bold", 10))
            labe.grid(column=0, row=10) 
        elif check_state.get() == True and  check_stateOne.get() == True: #If both write and display selected
            csvDf.to_csv(os.path.join(directory2, str(txtThree.get())), header=None, index=None)
            labetwo = Label(window, text="Results displayed and csv saved successfully in location", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=10) 
        else : #If only display selected
            labethree = Label(window, text="Results displayed successfully", font=("Arial Bold", 10))
            labethree.grid(column=0, row=10) 
        a = a + 1
    #---------------------------------------------------------------------------------------------------------------------------------
    #Clear Function
    def clear() :
        global canv #Get canvas from global environment
        global a #Get a value from global environment
        if a == 1: #a will only be one if the display portion is empty
            tk.messagebox.showinfo("Error", "No data to clear!")
            return
        for widget in canv.winfo_children(): #Destroy all widgets in canvas
            widget.destroy()
        canv = VerticalScrolledFrame(window, width=1000, borderwidth=1, relief=tk.SUNKEN, background="light gray") #Create new canvas
        canv.grid(column=0, row=11) # place canvas on grid
        a = 1 #set row count back to 1
        for displ in window.grid_slaves():
            if int(displ.grid_info()["row"]) == 10: #Get rid of row 9 label, or success indicator
                 displ.grid_forget()
        labetwo = Label(window, text="All values cleared successfully", font=("Arial Bold", 10)) #Label new success indicator for successfully clearing
        labetwo.grid(column=0, row=10)
    #---------------------------------------------------------------------------------------------------------------------------------
    #Clear Button
    btn = Button(window, text="Clear", command=clear)
    btn.grid(column=1, row=11)
    #---------------------------------------------------------------------------------------------------------------------------------
    #Process Button
    btn = Button(window, text="Process", command=process)
    btn.grid(column=0, row=9)
    #Run
    window.mainloop()
if __name__ == '__main__':
    main()

