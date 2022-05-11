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
import os
import csv
import astropy.io
#-------------------------------------------------------------------------------------------------------------------------------------
#Define entire code as a function, neccessary for turning into EXE
#CMD prompt to make executable : pyinstaller.exe --onefile --noconsole --icon=logoHeader.ico headereditor2.py 
def main():
    #---------------------------------------------------------------------------------------------------------------------------------
    #Portion to initialize and name window
    window = Tk()
    window.geometry('690x460') #Set window parameters
    window.title("FITS Header Editor 2.0") #name window
    #window.iconbitmap(logoHeader.ico)#set icon for program
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
    #Portion to initially place canvas on grid. This canvas will be destroyed and written over whenever the clear button is selected.
    #Canvas is defined globally so it can be destroyed in the clear function
    global canv
    canv = VerticalScrolledFrame(window, width=500, borderwidth=1, relief=tk.SUNKEN, background="light gray")#Initialize canvas with VSF function
    canv.grid(column=0, row=9) # set canvas on grid
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
    lbl = Label(window, text="FITS Header Editor 2.0", font=("Arial Bold", 10))#Set title variable
    lbl.grid(column=0, row=0)#Place title on grid
    directory1Select = FolderSelect(window,"Choose folder to display/edit FITS header ") #Set directory select one
    directory1Select.grid(row=1) #Place on grid
    lblTwo = Label(window, text="Enter the keyword you would like to look for", font=("Arial Bold", 10)) #Label for txt entry window
    lblTwo.grid(column=0, row=2) #Place label on grid
    txt = Entry(window,width=10) #Entry window for keyword
    txt.grid(column=1, row=2) #Place entry window on grid
    ask = Label(window, text="Would you like to write to csv, display, and/or edit?", font=("Arial Bold", 10)) #Label for check boxes
    ask.grid(column=0, row=3) #Place label on grid
    chk_state = BooleanVar() #Make check state true or false variable
    chk_state.set(False) #Have check box set to false upon opening window
    chk_stateOne = BooleanVar() #^
    chk_stateOne.set(False)#^
    chk_stateTwo = BooleanVar()#^
    chk_stateTwo.set(False)#^
    chk = Checkbutton(window, text='Display', var=chk_state) #Set first check box and assign to boolean variable
    chk.grid(column=1, row=3) #Place check box on grid
    chkOne = Checkbutton(window, text='Edit', var=chk_stateOne) #Set second check box and assign to boolean variable
    chkOne.grid(column=2, row=3) #Place check box on grid
    chkTwo = Checkbutton(window, text='Write', var=chk_stateTwo) #Set third check box and assign to boolean variable
    chkTwo.grid(column=3, row=3) #Place check box on grid
    lblTwo = Label(window, text="If edit, what would you like to change the keyword to?", font=("Arial Bold", 10)) #Label for edit keyword entry window
    lblTwo.grid(column=0, row=4) #Place label on grid
    txtTwo = Entry(window,width=10) #Entry window for lbltwo
    txtTwo.grid(column=1, row=4) #Place entry window on grid
    lblTwo = Label(window, text="If write, what would you like to name your csv file? (Format : example.csv)", font=("Arial Bold", 10)) #Label for naming csv file entry window
    lblTwo.grid(column=0, row=5) #Place label on grid
    txtThree = Entry(window,width=10) #entry window for naming csv file
    txtThree.grid(column=1, row=5) #Place entry window on grid
    directory2Select = FolderSelect(window,"If write, choose location to save csv ") #Call directory select function to save csv to certain location
    directory2Select.grid(row=6) #Place directory select on grid
    #---------------------------------------------------------------------------------------------------------------------------------
    #Set count variable
    #Set count as global so it can be used in process and clear with value set to one upon running the program. After initially running the program,
    #these two lines will not be ran through again. This variable is for placing labels on canvas. Every time a label is placed, count increases. 
    #If the clear button is selected, count is set back to one so, when the process button is pressed again, count will start by placing label on first row in canvas
    global count
    count = 1 #Count set to one outside of process function
    #---------------------------------------------------------------------------------------------------------------------------------
    #Process function for all reasonable actions desired by user
    def process():
        global count #Call count global again so function recognizes count when called upon
        g = 0 #Variable created for exiting function out of a for loop -explained in more detail when called upon
        #-----------------------------------------------------------------------------------------------------------------------------
        #Error Handling : All error messages kill the process function with return statement
        if chk_stateTwo.get() != True and chk_stateOne.get() != True and chk_state.get() != True: #Error if no check box is checked
            tk.messagebox.showinfo("Error" , "Choose Write, Edit, or Display") 
            return
        if directory1Select.folder_path == '': #Error if no directory is entered to parse through
            tk.messagebox.showinfo("Error", "Enter a directory")
            return
        if chk_stateOne.get() == True and str(txtTwo.get()) == '': #Error if edit selected but no new value entered
            tk.messagebox.showinfo("Error", "Enter new value for chosen keyword")
            return
        if str(txt.get()) == '': #Error if no object to search for entered
            tk.messagebox.showinfo("Error", "Enter keyword to search for")
            return
        if str(txtThree.get()) == '' and chk_stateTwo.get() == True : #Error if write and no name for csv file
            tk.messagebox.showinfo("Error", "Enter name to save csv file")
            return
        if '.csv' not in str(txtThree.get()) and chk_stateTwo.get() == True : #Error if csv file name entered is not properly formatted
           tk.messagebox.showinfo("Error", "Please format csv file as follows : example.csv")
           return 
        if directory2Select.folder_path == '' and chk_stateTwo.get() == True : #Error if write selected and no location to enter csv entered
            tk.messagebox.showinfo("Error", "Enter directory to save csv file")
            return
        #-----------------------------------------------------------------------------------------------------------------------------
        #The only time that there will be a widget in row 8 is after the code has been cleared or process has been ran
        #Row 8 is for displaying messages that confirm the action desired has been completed. For example, if row 8 says "All values 
        #cleared successfuly", at this point in the process function that will be cleared, so another label, like "values
        #successfuly displayed" can be placed in row 8
        for displ in window.grid_slaves(): 
            if int(displ.grid_info()["row"]) == 8:
                 displ.grid_forget()
        #-----------------------------------------------------------------------------------------------------------------------------
        #Get values from all entries. If the values are not needed, ie. newVal when the user doesn't select to input a new value,
        #the value will simply not be used
        directory = directory1Select.folder_path        
        directory2 = directory2Select.folder_path
        keyWord = str(txt.get())
        newVal = str(txtTwo.get())
        name = str(txtThree.get())
        err = 0 #Variable created to notify user if there are no FTS files in entered directory, explained further when called upon
        #-----------------------------------------------------------------------------------------------------------------------------
        #All values that are entered to csv file are put into a data frame, which is INITIALIZED here. Data frame has axis titles
        #to keep all data in order, but the actual titles displayed in the csv file are placed in the first row of the dataframe.
        #This was done because dataframes are formatted in a way that both row and column axes have titles. Although it's
        #possible to just title the column axis as Object and have each row axis be the filename, this causes (1,1) in the csv file to
        #be an empty cell
        csvDf = pd.DataFrame({'File Name' : [], 'Object': []}) #initialize dataframe
        frame = pd.DataFrame({'File Name': ['File Name'], 'Object': ['Object']}) #enter dataframe titles
        csvDf = [csvDf, frame] #create structure for concatenation
        csvDf = pd.concat(csvDf) #concatenate
        #-----------------------------------------------------------------------------------------------------------------------------
        #For loop that iterates through each file and completes neccesary actions
        os.chdir(directory) #change to input directory so files can be found
        for filename in os.listdir(directory): #iterate through files in directory
            if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"): #only iterate through FTS files
                x = fits.open(os.path.join(directory, filename)); #open FTS file
                x = x[0].header #get header information from FTS file
                #---------------------------------------------------------------------------------------------------------------------
                #More error handling. If the inputed keyword cannot be found in file, show message box
                if keyWord not in x :
                    tk.messagebox.showinfo("Error", "Keyword not found in" + str(filename))
                    ask = tk.messagebox.askquestion("Error", "Would you like to continue parsing the directory") #ask user if they would 
                    #like to kill the function or if they would like to ignore the file without the keyword and keep looking for it in
                    #other files
                    if ask == 'yes':
                        continue; #Keep parsing if user chooses to
                    else:
                        g = 1 #set g to one
                        break #break for loop
                err = err + 1 #add one to err. This is done inside of the for loop and can only be added to if there is a FITS file inside of the directory
                #---------------------------------------------------------------------------------------------------------------------
                #Section for displaying, writing, and/or editing. Edit comes before all, so values are edited before being displayed and/or written
                if chk_stateOne.get() == True:#If edit, change values before displaying
                    fits.setval(filename, keyWord,value=newVal) #Change header value to new value
                if chk_stateTwo.get() == True:#If write, add each files info to dataframe
                    frame = pd.DataFrame({'File Name': [str(filename)], 'Object': [str(fits.getval(filename, keyWord))]}) #Enter information
                    csvDf = [csvDf, frame] #create structure for concatenation
                    csvDf = pd.concat(csvDf) #concatenate
                if chk_state.get() == True:#If display, display on same window all values
                    displ = Label(canv, text=str(filename) + " : " + str(fits.getval(filename, keyWord)), font=("Arial Bold", 10)) #Add as label on canvas
                    displ.grid(column=0, row=count) #set on grid at row which is defined by global count
                    count = count + 1 #Add to count if displaying
            else:
                continue
        #-----------------------------------------------------------------------------------------------------------------------------
        #Variables for exiting out of function
        if g == 1 : #If the user has found that the keyword cant be found, and they don't want to keep looking through the file, this will
        #exit out of the function after the for loop has been exited out of
            return
        if err == 0 : #Variable will only be 0 if no files contain FTS images
            tk.messagebox.showinfo("Error", "Directory doesn't contain FTS files")
            return
        #-----------------------------------------------------------------------------------------------------------------------------
        #Write to csv, display different variation of success in row 8
        if chk_stateTwo.get() == True: #If only write selected
            csvDf.to_csv(os.path.join(directory2, str(txtThree.get())), header=None, index=None) #Write dataframe to csv without axis titles
        if chk_stateTwo.get() == True and chk_stateOne.get() != True and chk_state.get() != True: #Success label for only write
            #This can't be added to the previous if statement due to the additional requirements
            labetwo = Label(window, text="CSV saved successfully in input location", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8)
        if chk_stateTwo.get() == True and chk_stateOne.get() == True and chk_state.get() != True: #Success label for write and edit
            labetwo = Label(window, text="Values edited and CSV saved successfully in input location", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
        if chk_stateTwo.get() != True and chk_stateOne.get() == True and chk_state.get() == True: #Success label for display and edit
            labetwo = Label(window, text="Values edited and displayed successfully", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
        if chk_stateTwo.get() != True and chk_stateOne.get() == True and chk_state.get() != True: #Success label for only edit
            labetwo = Label(window, text="Values edited successfully", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
        if chk_stateTwo.get() != True and chk_stateOne.get() != True and chk_state.get() == True: #Success label for only display
            labetwo = Label(window, text="Values displayed successfully", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
        if chk_stateTwo.get() == True and chk_stateOne.get() != True and chk_state.get() == True: #Success label for write and display
            labetwo = Label(window, text="CSV saved and values displayed successfully", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
        if chk_stateTwo.get() == True and chk_stateOne.get() == True and chk_state.get() == True: #Success label for write, display, and edit
            labetwo = Label(window, text="CSV saved, values edited and displayed successfully", font=("Arial Bold", 10))
            labetwo.grid(column=0, row=8) 
    #---------------------------------------------------------------------------------------------------------------------------------
    #Clear Function
    def clear() :
        global canv #Get canvas from global environment
        global count #Get count value from global environment
        if count == 1: #Count will only be one if the display portion is empty
            tk.messagebox.showinfo("Error", "No data to clear!")
            return #exit function
        for widget in canv.winfo_children(): #Destroy all widgets in canvas
            widget.destroy()
        canv = VerticalScrolledFrame(window, width=500, borderwidth=1, relief=tk.SUNKEN, background="light gray") #Create a new canvas in the same position
        canv.grid(column=0, row=9)
        count = 1 #set count back to one so next display will start in the first row
        for displ in window.grid_slaves(): #Get rid of row 8 label, or success indicator
            if int(displ.grid_info()["row"]) == 8:
                 displ.grid_forget()
        labetwo = Label(window, text="All values cleared successfully", font=("Arial Bold", 10)) #Make new success label for clearing
        labetwo.grid(column=0, row=8) #Place success label for clearing in row 8 of grid
    #---------------------------------------------------------------------------------------------------------------------------------
    #Clear Button
    btn = Button(window, text="Clear", command=clear) #Initialize clear button, assign command as clear function
    btn.grid(column=1, row=9) #place clear button on grid 
    #---------------------------------------------------------------------------------------------------------------------------------
    #Process button
    btn = Button(window, text="Process", command=process) #Initialize process button, assign command as process function
    btn.grid(column=0, row=7) #place process button on grid
    #---------------------------------------------------------------------------------------------------------------------------------
    #Run
    window.mainloop()
if __name__ == '__main__':
    main()