from toolbox.InventoryClass import *
from datetime import datetime

from camera.register_user.registerUser import *
import subprocess

from camera.employee_verification.verification import Verification

[ScaleWidth, ScaleHeight] = windowSize()
SectionSizes = retreiveSectionSizes()
SectionLoc = retreiveSectionLoc()
FontSizes = retrievefontSizes()
allColors = retrieveColors()


def start_camera(parent):
    dispUserField = Frame(parent, bg=allColors["grey"][0])
    dispUserField.place(x=SectionLoc["read"][0], y=SectionLoc["read"][1], width=SectionLoc["read"][2],
                        height=SectionLoc["read"][3])

    barcode_facial_verification = Verification()
    global user_id
    user_id = barcode_facial_verification.run_verification()

    dispUserFieldtxt = Label(parent, text=user_id, font=("", FontSizes[1]),
                             fg=allColors['black'][0], bg=allColors["grey"][0])
    dispUserFieldtxt.place(x=SectionLoc["readBut"][0], y=SectionLoc["readBut"][1])

    


class Details_Button(Button):
    def __init__(self, parent3, parent1, inv, text, level, item, **kwargs):
        self.text = text
        self.level = level
        self.item = item
        self.inv = inv
        self.parent1 = parent1
        super().__init__(parent3)
        self['text'] = self.text
        self['command'] = lambda: self.comnd(self.item)

    def comnd(self, item):
        # print(item[0])
        self.clear(self.parent1)

        self.itemSel = Label(self.parent1, text=item[0], font=("", FontSizes[0], "bold"),
                             fg=allColors['black'][0], bg=allColors['window'][0])
        self.itemSel.place(x=SectionLoc["itemSel"][0], y=SectionLoc["itemSel"][1])

        self.displayItemDetails1 = Label(self.bodyframe2, text='Status: ' + item[2], font=("", FontSizes[3], "bold"),
                                         fg=allColors['black'][0], bg=self.bf2color)
        self.displayItemDetails1.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.displayItemDetails2 = Label(self.bodyframe3, text='User: ' + item[3], font=("", FontSizes[3], "bold"),
                                         fg=allColors['black'][0], bg=allColors['bodyframe3'][0])
        self.displayItemDetails2.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.displayItemDetails3 = Label(self.bodyframe4, text='Cond: ' + item[4], font=("", FontSizes[3], "bold"),
                                         fg=allColors['black'][0], bg=allColors['bodyframe4'][0])
        self.displayItemDetails3.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.referenceFrames = [self.parent1, self.bodyframe2, self.bodyframe3, self.bodyframe4]
        if item[2] == "Available":

            self.dispUserField = Frame(self.referenceFrames[1], bg=allColors["grey"][0])
            self.dispUserField.place(x=SectionLoc["read"][0], y=SectionLoc["read"][1], width=SectionLoc["read"][2],
                                     height=SectionLoc["read"][3])

            '''
            self.input_field = Entry(self.bodyframe2,font=("", FontSizes[1]))
            self.input_field.place(relx=0.45, rely=0.7, anchor=CENTER)
            self.input_field.focus_force() #"<FocusIn>",callback
            '''
            tempnameU = "self.displayItemDetails1." + item[0] + "Use"

            self.readBut = Button(self.referenceFrames[1], text='Read', bg=allColors['grey'][0],
                                  font=("", FontSizes[0]), bd=0, cursor='hand2',
                                  activebackground=allColors['white'][0],
                                  command=lambda: start_camera(self.referenceFrames[1]))
            self.readBut.place(relx=0.845, rely=0.71, anchor=CENTER)

            globals()[tempnameU] = Use_Button(self.referenceFrames, self.inv, self.level, item)
            globals()[tempnameU].place(relx=0.85, rely=0.85, anchor=CENTER)
        elif item[2] == "In Use":
            tempnameR = "self.displayItemDetails1." + item[0] + "Return"
            globals()[tempnameR] = Return_Button(self.referenceFrames, self.inv, self.level, item)
            globals()[tempnameR].place(relx=0.5, rely=0.85, anchor=CENTER)

    def clear(self, parent1):

        self.bodyframes = [SectionSizes["bodyframe1"], SectionSizes["bodyframe2"],
                           SectionSizes["bodyframe3"], SectionSizes["bodyframe4"]]

        self.clearItmColor = allColors['window'][0]
        self.clearItm = Frame(parent1, bg=self.clearItmColor)
        self.clearItm.place(x=SectionLoc["bodyframe2"][2], y=SectionLoc["bodyframe2"][3],
                            width=self.bodyframes[1][2],
                            height=self.bodyframes[1][3])

        self.bf2color = allColors['bodyframe2'][0]
        self.bodyframe2 = Frame(parent1, bg=self.bf2color)
        self.bodyframe2.place(x=SectionLoc["bodyframe2"][0], y=SectionLoc["bodyframe2"][1],
                              width=self.bodyframes[1][0],
                              height=self.bodyframes[1][1])

        self.bf3color = allColors['bodyframe3'][0]
        self.bodyframe3 = Frame(parent1, bg=self.bf3color)
        self.bodyframe3.place(x=SectionLoc["bodyframe3"][0], y=SectionLoc["bodyframe3"][1],
                              width=self.bodyframes[2][0],
                              height=self.bodyframes[2][1])
        self.bf4color = allColors['bodyframe4'][0]
        self.bodyframe4 = Frame(parent1, bg=self.bf4color)
        self.bodyframe4.place(x=SectionLoc["bodyframe4"][0], y=SectionLoc["bodyframe4"][1],
                              width=self.bodyframes[3][0],
                              height=self.bodyframes[3][1])


class Use_Button(Button):
    def __init__(self, parent1, inv, level, item, **kwargs):
        self.inv = inv
        self.level = int(level)
        self.item = item
        self.parent1 = parent1
        # self.username = user
        super().__init__(parent1[1])
        self['text'] = 'Use'
        self['command'] = lambda: self.cUse(self.item)

    def cUse(self, item):
        # self.usernameText = self.username.get()
        global user_id
        print("user id: " + user_id)
        self.usernameText = user_id
        self.parent1[0].focus_force()
        if len(self.usernameText) >= 1:
            self.lvlSel = self.inv.listLevels[self.level - 1]
            self.lvlSel.use_item(item[0], self.usernameText, str(datetime.now())[:21])
            self.inv.save_log()
            self.inv.add_records(self.usernameText, item[0], 'Level ' + str(self.level), 'In Use',
                                 str(datetime.now())[:21])
            print(item[0] + ' in use')
            Manager(self.parent1[0], self.level)


class Return_Button(Button):
    def __init__(self, parent1, inv, level, item, **kwargs):
        self.inv = inv
        self.level = int(level)
        self.item = item
        self.parent1 = parent1
        super().__init__(parent1[1])
        self['text'] = 'Return'
        self['command'] = lambda: self.cRet(self.item)

    def cRet(self, item):
        self.lvlSel = self.inv.listLevels[self.level - 1]
        self.lvlSel.ret_item(item[0], str(datetime.now())[:21])
        self.inv.save_log()
        self.inv.add_records(item[3], item[0], 'Level ' + str(self.level), 'Returned', str(datetime.now())[:21])
        print(item[0] + ' Returned')
        globalLevel = self.level
        Manager(self.parent1[0], self.level)


class Remove_Button(Button):
    def __init__(self, parent3, parent1, image, bg, inv, level, item, **kwargs):
        self.level = int(level)
        self.item = item
        self.parent1 = parent1
        self.image = image
        self.bg = bg
        self.inv = inv
        super().__init__(parent3)
        self['image'] = self.image
        self['bg'] = self.bg
        self['command'] = lambda: self.cRem(self.item)

    def cRem(self, item):
        with open('load/inventory.json', 'r') as file:
            data = json.load(file)
        del data['Level ' + str(self.level)]['items'][item[0]]
        data['Level ' + str(self.level)]['Empty'].append(int(item[1][-1]))
        data['Level ' + str(self.level)]['Empty'].sort()
        if item[2] == 'Available':
            data['Level ' + str(self.level)]['Available'].remove(item[0])
        else:
            data['Level ' + str(self.level)]['In Use'].remove(item[0])

        with open("load/inventory.json", "w") as write_file:
            json.dump(data, write_file)

        self.inv.add_records('-', item[0], 'Level ' + str(self.level), 'Removed', str(datetime.now())[:21])
        print(item[0] + ' Removed')
        globalLevel = self.level
        Manager(self.parent1, self.level)


class Add_Button(Button):
    def __init__(self, itemframe, bodyframe, window, selIf, image, bg, inv, level, **kwargs):
        self.level = int(level)
        self.parent1 = window
        self.parent2 = bodyframe
        self.itf = itemframe
        self.image = image
        self.bg = bg
        self.a = selIf
        self.inv = inv
        super().__init__(itemframe)
        self['image'] = self.image
        self['bg'] = self.bg
        self['command'] = lambda: self.cAdd()

    def cAdd(self):
        self.clearItm = Frame(self.parent2, bg=allColors['itemframe'][0])
        self.clearItm.place(x=SectionLoc["itemframes"][self.a][0],
                            y=SectionLoc["itemframes"][self.a][1],
                            width=SectionLoc["itemframes"][self.a][2],
                            height=SectionLoc["itemframes"][self.a][3])

        self.lbl = Label(self.clearItm, text='Item: ', font=("", FontSizes[1], "bold"),
                         fg=allColors['black'][0], bg=allColors['itemframe'][0])
        self.lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.input_field = Entry(self.clearItm, font=("", FontSizes[1]))
        self.input_field.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.input_field.focus_force()  # "<FocusIn>",callback
        pop2 = subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)

        self.submit = SecAdd_Button(self.clearItm, self.parent1, self.inv, self.level, self.input_field, pop2)
        self.submit.place(relx=0.5, rely=0.88, anchor=CENTER)


class SecAdd_Button(Button):
    def __init__(self, parent, parent1, inv, level, item_name, pop2, **kwargs):
        self.inv = inv
        self.level = level
        self.text = 'Add'
        self.parent1 = parent1
        self.osk2 = pop2
        self.itemNameField = item_name
        super().__init__(parent)
        self['text'] = self.text
        self['command'] = lambda: self.cfmAdd(self.itemNameField)

    def cfmAdd(self, itemNameField):
        self.itemName = itemNameField.get()
        self.osk2.kill()
        self.parent1.focus_force()
        self.lvlSel = self.inv.listLevels[self.level - 1]
        self.itemsToAdd = []
        self.itemsToAdd.append(self.itemName)
        self.lvlSel.add_items(self.itemsToAdd)
        self.inv.save_log()
        self.inv.add_records('-', self.itemName, 'Level ' + str(self.level), 'Added', str(datetime.now())[:21])
        print(self.itemName + ' Added')
        globalLevel = self.level
        Manager(self.parent1, self.level)

class Register_Button(Button):
    def __init__(parent, idstr, self=None, **kwargs):
        self.text = 'Register'
        self.idstr = idstr
        super().__init__(parent)
        self['text'] = self.text
        self['command'] = lambda: parent.register_user(self.idstr)
    def register_user(a):
        addNewPerson(a)
        
        
    
class Table:
    def __init__(self, parent, listRec):
        # code for creating table
        self.total_rows = len(listRec)
        try:
            self.total_columns = len(listRec[0])
            if self.total_rows > 11:
                self.total_rows = 11
            self.listRec = listRec
            if self.listRec[0] != ["User", "Item", "Level", "Status", "Date"]:
                self.listRec.insert(0, ["User", "Item", "Level", "Status", "Date"])
            for i in range(self.total_rows + 1):
                for j in range(self.total_columns):
                    if i == 0:
                        self.e = Entry(parent, width=24, fg='blue',
                                       font=('', FontSizes[0], 'bold'))
                        self.e.grid(row=i, column=j)
                        self.e.insert(END, self.listRec[i][j])
                    else:
                        self.e = Entry(parent, width=24, fg='black',
                                       font=('', FontSizes[0], ''))
                        self.e.grid(row=i, column=j)
                        self.e.insert(END, self.listRec[i][j])
        except:
            print("Records are empty.")


class Manager:
    def __init__(self, window, lastLevel=1):
        self.window = window
        self.window.title('Smart Toolbox Inventory')
        self.windowWidth = self.window.winfo_screenwidth()
        self.windowHeight = self.window.winfo_screenheight()
        # print(self.windowWidth, self.windowHeight)
        self.window.geometry(f'{self.windowWidth}x{self.windowHeight}')
        self.ScaleWidth = ScaleWidth
        self.ScaleHeight = ScaleHeight
        self.window.state('zoomed')
        self.allColors = allColors
        self.window.config(background=allColors['window'][0])
        self.lastLevel = lastLevel
        # window icon
        icon = PhotoImage(file='gui\\images\\toolbox.png')
        self.window.iconphoto(True, icon)

        self.SectionSizes = SectionSizes
        self.SectionLoc = SectionLoc
        self.FontSizes = FontSizes

        # ================================
        # =========Header=================
        # ================================
        # default bg = '#009df4'
        self.header = Frame(self.window, bg=self.allColors['header'][0])
        self.headerWidth = int(self.SectionSizes["header"][0])
        self.headerHeight = int(self.SectionSizes["header"][1])
        self.header.place(x=self.SectionLoc["header"][0], y=self.SectionLoc["header"][1],
                          width=self.headerWidth,
                          height=self.headerHeight)

        # default activebackground='#32cf8e'
        self.exit_text = Button(self.header, text='Exit', bg=allColors['exit'][0], font=("", FontSizes[1], "bold"),
                                bd=0,
                                fg='white', cursor='hand2', activebackground=self.allColors['exit'][1],
                                command=lambda: self.window.quit())
        self.exit_text.place(x=self.SectionLoc["exit"][0], y=self.SectionLoc["exit"][1])

        # ================================
        # =========SideBar================
        # ================================     

        self.sidebar = Frame(self.window, bg=self.allColors['sidebar'][0])
        self.sidebarWidth = self.SectionSizes["sidebar"][0]
        self.sidebarHeight = self.SectionSizes["sidebar"][1]
        self.sidebar.place(x=SectionLoc["sidebar"][0], y=SectionLoc["sidebar"][1], width=self.sidebarWidth,
                           height=self.sidebarHeight)

        # ================================
        # =========Body===================
        # ================================    

        self.heading = Label(self.window, text='Toolbox Inventory', font=("", self.FontSizes[2], "bold"),
                             fg=self.allColors['heading'][0],
                             bg=self.allColors['heading'][1])
        self.heading.place(x=SectionLoc["heading"][0], y=SectionLoc["heading"][1])

        # ================================
        # =========BodyFrames=============
        # ================================ 

        self.bodyframes = [self.SectionSizes["bodyframe1"], self.SectionSizes["bodyframe2"],
                           self.SectionSizes["bodyframe3"], self.SectionSizes["bodyframe4"]]

        def clearbf1():
            self.bf1color = self.allColors['bodyframe1'][0]
            self.bodyframe1 = Frame(self.window, bg=self.bf1color)
            self.bodyframe1.place(x=SectionLoc["bodyframe1"][0], y=SectionLoc["bodyframe1"][1],
                                  width=self.bodyframes[0][0],
                                  height=self.bodyframes[0][1])

        '''
        #default bg='#009aa5'
        self.bodyframe2= Frame(self.window, bg='#406e8e')
        self.bodyframe2.place(x=int(self.ScaleWidth*0.24), 
                                y=int(self.ScaleHeight*0.068),
                                width=self.bodyframes[1][0],
                                height=self.bodyframes[1][1])
        '''

        def clearbf2():
            self.bf2color = self.allColors['bodyframe2'][0]
            self.bodyframe2 = Frame(self.window, bg=self.bf2color)
            self.bodyframe2.place(x=SectionLoc["bodyframe2"][0], y=SectionLoc["bodyframe2"][1],
                                  width=self.bodyframes[1][0],
                                  height=self.bodyframes[1][1])

            self.clearItm = Frame(self.window, bg=self.allColors['bodyframe2'][1])
            self.clearItm.place(x=SectionLoc["bodyframe2"][2], y=SectionLoc["bodyframe2"][3],
                                width=self.bodyframes[1][2],
                                height=self.bodyframes[1][3])

        def clearbf3():
            self.bf3color = self.allColors['bodyframe3'][0]
            self.bodyframe3 = Frame(self.window, bg=self.bf3color)
            self.bodyframe3.place(x=SectionLoc["bodyframe3"][0], y=SectionLoc["bodyframe3"][1],
                                  width=self.bodyframes[2][0],
                                  height=self.bodyframes[2][1])

        def clearbf4():
            self.bf4color = self.allColors['bodyframe4'][0]
            self.bodyframe4 = Frame(self.window, bg=self.bf4color)
            self.bodyframe4.place(x=SectionLoc["bodyframe4"][0], y=SectionLoc["bodyframe4"][1],
                                  width=self.bodyframes[3][0],
                                  height=self.bodyframes[3][1])

        clearbf1()
        clearbf2()
        clearbf3()
        clearbf4()

        # Logo
        self.logoImage = Image.open('gui\\images\\toolbox.png')
        self.logoImageW, self.logoImageH = self.logoImage.size
        self.logoImage = self.logoImage.resize((SectionLoc["logo"][2], SectionLoc["logo"][3]))
        photo = ImageTk.PhotoImage(self.logoImage)
        self.logo = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.logo.image = photo
        self.logo.place(x=SectionLoc["logo"][0], y=SectionLoc["logo"][1])

        # Name of brand/person
        self.brandName = Label(self.sidebar, text='D&I TinkerSpace', bg=self.allColors['white'][0],
                               font=("", self.FontSizes[2], "bold"))
        self.brandName.place(x=SectionLoc["brandName"][0], y=SectionLoc["brandName"][1])

        # Display Inventory in Level
        self.Toolbox = Toolbox()
        try:
            self.Toolbox.load_log()
        except:
            print("No load json file found. Initialising empty file")

        def inv_save(*args):
            print('save')
            self.Toolbox.save_log()

        def inv_load(*args):
            print('load')
            self.Toolbox.load_log()
            
        def get_Uid(input_id,pop_id):
            pop_id.kill()
            emp_id = input_id.get()
            if len(emp_id)==8:
                addNewPerson(emp_id)
            
        def reg_u(*args):
            print('Add New User')
            clearbf1()
            clearbf2()
            clearbf3()
            clearbf4()
            self.newUserRegistration = Label(self.bodyframe1, text='Employee ID :', font=("", self.FontSizes[2], "bold"),
                                                fg=self.allColors['black'][0],
                                                bg=self.allColors['bodyframe1'][0])
                                                
            self.newUserRegistration.place(x=SectionLoc["registerUN"][0], y=SectionLoc["registerUN"][1])
            
            #Input Field for Employee ID
            self.input_id = Entry(self.bodyframe1, font=("", FontSizes[2]),bg=self.allColors['itemframe'][0])
            self.input_id.place(x=SectionLoc["registerUid"][0], y=SectionLoc["registerUid"][1])
            self.input_id.focus_force()  # "<FocusIn>",callback
            pop_id = subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)
            
            #Get Employee ID
            self.get_id = Button(self.bodyframe1, text="Save", bg=self.allColors['itemframe'][0],
                                font=("", self.FontSizes[2], "bold"),
                                bd=0,
                                activebackground=self.allColors['white'][0], command= lambda:get_Uid(self.input_id,pop_id))
            self.get_id.place(x=SectionLoc["getUid"][0], y=SectionLoc["getUid"][1])
            #addNewPerson(input("Enter Employee Id: "))

            
        # Inventory
        self.dashboardImage = Image.open('gui\\images\\tray.png')
        self.dashboardImageW, self.dashboardImageH = self.dashboardImage.size
        self.dashboardImage = self.dashboardImage.resize((SectionLoc["sidebar"][2], SectionLoc["sidebar"][3]))
        photo = ImageTk.PhotoImage(self.dashboardImage)
        self.dashboard = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.dashboard.image = photo
        self.dashboard.place(x=SectionLoc["dashboard"][0], y=SectionLoc["dashboard"][1])

        self.dashboard_text = Button(self.sidebar, text='Inventory', bg=self.allColors['white'][0],
                                     font=("", self.FontSizes[2], "bold"), bd=0, cursor='hand2',
                                     activebackground=self.allColors['white'][0], command=lambda: Manager(self.window))
        self.dashboard_text.place(x=SectionLoc["dashboardText"][0], y=SectionLoc["dashboardText"][1])

        # Save
        self.saveImage = Image.open('gui\\images\\save.jpg')
        self.saveImageW, self.saveImageH = self.saveImage.size
        self.saveImage = self.saveImage.resize((SectionLoc["sidebar"][2], SectionLoc["sidebar"][3]))
        photo = ImageTk.PhotoImage(self.saveImage)
        self.save = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.save.image = photo
        self.save.place(x=SectionLoc["save"][0], y=SectionLoc["save"][1])

        self.save_text = Button(self.sidebar, text="Save", bg=self.allColors['white'][0],
                                font=("", self.FontSizes[2], "bold"),
                                bd=0,
                                activebackground=self.allColors['white'][0], command=inv_save)
        self.save_text.place(x=SectionLoc["save"][2], y=SectionLoc["save"][3])

        # Register
        self.registerImage = Image.open('gui\\images\\register.png')
        self.registerImageW, self.registerImageH = self.registerImage.size
        self.registerImage = self.registerImage.resize((SectionLoc["sidebar"][2], SectionLoc["sidebar"][3]))
        photo = ImageTk.PhotoImage(self.registerImage)
        self.register = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.register.image = photo
        self.register.place(x=SectionLoc["refresh"][0], y=SectionLoc["refresh"][1])

        self.register_json = Button(self.sidebar, text="Register", bg=self.allColors['white'][0],
                                   font=("", self.FontSizes[2], "bold"), bd=0,
                                   activebackground=self.allColors['white'][0], command=reg_u)
        self.register_json.place(x=SectionLoc["refresh"][2], y=SectionLoc["refresh"][3])

        # Records

        def load_rec(*args):
            clearbf1()
            clearbf2()
            clearbf3()
            clearbf4()

            self.dispRecords = Table(self.bodyframe1, self.Toolbox.records)

        self.recordsImage = Image.open('gui\\images\\records.png')
        self.recordsImageW, self.recordsImageH = self.recordsImage.size
        self.recordsImage = self.recordsImage.resize((SectionLoc["sidebar"][2], SectionLoc["sidebar"][3]))
        photo = ImageTk.PhotoImage(self.recordsImage)
        self.records = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.records.image = photo
        self.records.place(x=SectionLoc["records"][0], y=SectionLoc["records"][1])

        self.records_access = Button(self.sidebar, text="Records", bg=self.allColors['white'][0],
                                     font=("", self.FontSizes[2], "bold"), bd=0,
                                     activebackground=self.allColors['white'][0], command=load_rec)
        self.records_access.place(x=SectionLoc["records"][2], y=SectionLoc["records"][3])

        # BodyFrame1 Dropdown menu
        self.trayLevels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7"]
        self.currentLevel = StringVar()
        self.currentLevel.set(self.trayLevels[self.lastLevel - 1])
        self.levelsSelect = OptionMenu(self.bodyframe1, self.currentLevel, *self.trayLevels)
        self.levelsSelect.config(height=1, font=("", self.FontSizes[0], "bold"))
        self.levelsSelect.place(x=SectionLoc["trayLevels"][0], y=SectionLoc["trayLevels"][1])

        # Item Frames self.itemframe1-8
        def disp_itemframes():
            self.itfcolor = self.allColors['itemframe'][0]
            self.itemframe1 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe1.place(x=SectionLoc["itemframes"][0][0],
                                  y=SectionLoc["itemframes"][0][1],
                                  width=SectionLoc["itemframes"][0][2],
                                  height=SectionLoc["itemframes"][0][3])

            self.itemframe2 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe2.place(x=SectionLoc["itemframes"][1][0],
                                  y=SectionLoc["itemframes"][1][1],
                                  width=SectionLoc["itemframes"][1][2],
                                  height=SectionLoc["itemframes"][1][3])

            self.itemframe3 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe3.place(x=SectionLoc["itemframes"][2][0],
                                  y=SectionLoc["itemframes"][2][1],
                                  width=SectionLoc["itemframes"][2][2],
                                  height=SectionLoc["itemframes"][2][3])

            self.itemframe4 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe4.place(x=SectionLoc["itemframes"][3][0],
                                  y=SectionLoc["itemframes"][3][1],
                                  width=SectionLoc["itemframes"][3][2],
                                  height=SectionLoc["itemframes"][3][3])

            self.itemframe5 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe5.place(x=SectionLoc["itemframes"][4][0],
                                  y=SectionLoc["itemframes"][4][1],
                                  width=SectionLoc["itemframes"][4][2],
                                  height=SectionLoc["itemframes"][4][3])

            self.itemframe6 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe6.place(x=SectionLoc["itemframes"][5][0],
                                  y=SectionLoc["itemframes"][5][1],
                                  width=SectionLoc["itemframes"][5][2],
                                  height=SectionLoc["itemframes"][5][3])

            self.itemframe7 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe7.place(x=SectionLoc["itemframes"][6][0],
                                  y=SectionLoc["itemframes"][6][1],
                                  width=SectionLoc["itemframes"][6][2],
                                  height=SectionLoc["itemframes"][6][3])

            self.itemframe8 = Frame(self.bodyframe1, bg=self.itfcolor)
            self.itemframe8.place(x=SectionLoc["itemframes"][7][0],
                                  y=SectionLoc["itemframes"][7][1],
                                  width=SectionLoc["itemframes"][7][2],
                                  height=SectionLoc["itemframes"][7][3])

            self.itemframes = [self.itemframe1, self.itemframe2, self.itemframe3, self.itemframe4,
                               self.itemframe5, self.itemframe6, self.itemframe7, self.itemframe8]

        disp_itemframes()

        # Summary
        def disp_summary(*args):
            clearbf1()
            clearbf2()
            clearbf3()
            clearbf4()

            disp_itemframes()
            count = 0
            for level in self.Toolbox.listLevels:
                totalitems = str(len(level.available))
                levelSusmmary = level.name
                self.summaryLevel = Label(self.itemframes[count], text=levelSusmmary, font=("", FontSizes[1], "bold"),
                                          fg=self.allColors['black'][0], bg=self.itfcolor)
                self.summaryLevel.place(relx=0.5, rely=0.13, anchor=CENTER)
                if len(level.inUse) != 0:
                    y_loc = 0.3
                    for i in range(len(level.inUse)):

                        if i < 3:
                            textDet = level.inUse[i] + " :   " + level.item_user(level.inUse[i])
                            self.summaryLevelItem = Label(self.itemframes[count], text=textDet,
                                                          font=("", FontSizes[4], "bold"),
                                                          fg=self.allColors['orange'][0], bg=self.itfcolor)
                            self.summaryLevelItem.place(relx=0.5, rely=y_loc, anchor=CENTER)
                            y_loc += FontSizes[4] * 1.4 / 100
                        if i == 3:
                            textDet = "+"
                            self.summaryLevelItem = Label(self.itemframes[count], text=textDet,
                                                          font=("", FontSizes[4], "bold"),
                                                          fg=self.allColors['orange'][0], bg=self.itfcolor)
                            self.summaryLevelItem.place(relx=0.5, rely=y_loc, anchor=CENTER)

                textDet = "Available:  " + totalitems
                self.summaryLevelItem = Label(self.itemframes[count], text=textDet, font=("", FontSizes[5], "bold"),
                                              fg=self.allColors['green'][0], bg=self.itfcolor)
                self.summaryLevelItem.place(relx=0.5, rely=0.85, anchor=CENTER)

                count += 1

        self.summaryImage = Image.open('gui\\images\\summary.png')
        self.summaryImageW, self.summaryImageH = self.summaryImage.size
        self.summaryImage = self.summaryImage.resize((SectionLoc["sidebar"][2], SectionLoc["sidebar"][3]))
        photo = ImageTk.PhotoImage(self.summaryImage)
        self.summary = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
        self.summary.image = photo
        self.summary.place(x=SectionLoc["summary"][0], y=SectionLoc["summary"][1])

        self.summary_text = Button(self.sidebar, text='Summary', bg=self.allColors['white'][0],
                                   font=("", self.FontSizes[2], "bold"), bd=0,
                                   activebackground=self.allColors['white'][0], command=disp_summary)
        self.summary_text.place(x=SectionLoc["summary"][2], y=SectionLoc["summary"][3])

        def disp_indIframe(no, color):
            y_marker = 70
            if no > 5:
                y_marker = 210
                no -= 4
            self.itemframe8 = Frame(self.bodyframe1, bg=color)
            self.itemframe8.place(x=45 + 200 * (no - 1) + 50 * (no - 1),
                                  y=y_marker,
                                  width=SectionLoc["itemframes"][0][2],
                                  height=SectionLoc["itemframes"][0][3])

        # disp_indIframe(1,'#00FF00')

        # Troubleshooting
        # self.currentItems = getItemDetails(self.Toolbox.Level2.items)
        # print("Last level " + str(self.lastLevel))
        self.currentItems = self.Toolbox.retrieve_level(self.lastLevel).get_items()

        clearbf2()
        clearbf3()
        clearbf4()
        for i in range(8):

            checkerStr = str(i + 1)
            isEmpty = True
            for it in self.currentItems:
                if checkerStr == it[1][-1]:
                    isEmpty = False
                    tempnameF = 'self.itemframe' + checkerStr + 'item'
                    tempnameB = 'self.itemframe' + checkerStr + 'details'
                    tempnameMi = 'self.itemframe' + checkerStr + 'im'
                    tempnameM = 'self.itemframe' + checkerStr + 'remove'
                    globals()[tempnameMi] = resizeImage('gui\\images\\remove.jpg',
                                                        self.SectionLoc["addIm"][0],
                                                        self.SectionLoc["addIm"][1])
                    locals()[tempnameM] = Remove_Button(self.itemframes[i], self.window, globals()[tempnameMi],
                                                        self.allColors['bodyframe3'][0], self.Toolbox, self.lastLevel,
                                                        it)
                    locals()[tempnameM].place(relx=0.92, rely=0.88, anchor=CENTER)

                    # Details button for each item
                    globals()[tempnameB] = Details_Button(self.itemframes[i], self.window, self.Toolbox, 'Details',
                                                          self.lastLevel, it)
                    globals()[tempnameB].place(relx=0.5, rely=0.8, anchor=CENTER)

                    locals()[tempnameF] = Label(self.itemframes[i], text=it[0], font=("", FontSizes[6], "bold"),
                                                fg=self.allColors['black'][0], bg=self.itfcolor)
                    locals()[tempnameF].place(relx=0.5, rely=0.5, anchor=CENTER)
            if isEmpty:
                tempnameF = 'self.itemframe' + checkerStr + 'item'
                tempnamePi = 'self.itemframe' + checkerStr + 'im'
                tempnameP = 'self.itemframe' + checkerStr + 'add'
                globals()[tempnamePi] = resizeImage('gui\\images\\rsz_add.jpg',
                                                    self.SectionLoc["addIm"][0],
                                                    self.SectionLoc["addIm"][1])

                locals()[tempnameP] = Add_Button(self.itemframes[i], self.bodyframe1, self.window, i,
                                                 globals()[tempnamePi],
                                                 self.allColors['bodyframe3'][0], self.Toolbox, self.lastLevel)
                locals()[tempnameP].place(relx=0.92, rely=0.88, anchor=CENTER)

                locals()[tempnameF] = Label(self.itemframes[i], text="Empty", font=("", FontSizes[6], "bold"),
                                            fg=self.allColors['black'][0], bg=self.itfcolor)

                locals()[tempnameF].place(relx=0.5, rely=0.5, anchor=CENTER)

        # Each time the level is toggled, items are re-displayed
        def my_show(*args):

            disp_itemframes()
            clearbf2()
            clearbf3()
            clearbf4()

            # Retrieve Level Items
            self.varLevel = self.currentLevel.get()[-1]
            self.currentItems = self.Toolbox.retrieve_level(self.varLevel).get_items()

            # Iterate through each position
            self.itemlabels = []
            self.itembuttons = []
            for i in range(8):
                frame = self.itemframes[i]
                # Clear item frame after each selection of level
                checkerStr = str(i + 1)
                isEmpty = True

                for it in self.currentItems:
                    if checkerStr == it[1][-1]:
                        isEmpty = False
                        tempnameL = 'self.itemframe' + checkerStr + 'item'
                        tempnameB = 'self.itemframe' + checkerStr + 'details'
                        tempnameMi = 'self.itemframe' + checkerStr + 'im'
                        tempnameM = 'self.itemframe' + checkerStr + 'remove'
                        globals()[tempnameMi] = resizeImage('gui\\images\\remove.jpg',
                                                            self.SectionLoc["addIm"][0],
                                                            self.SectionLoc["addIm"][1])

                        globals()[tempnameM] = Remove_Button(frame, self.window, globals()[tempnameMi],
                                                             self.allColors['bodyframe3'][0], self.Toolbox,
                                                             self.varLevel, it)
                        globals()[tempnameM].place(relx=0.92, rely=0.88, anchor=CENTER)

                        # Details button for each item
                        globals()[tempnameB] = Details_Button(frame, self.window, self.Toolbox, 'Details',
                                                              self.varLevel, it)
                        globals()[tempnameB].place(relx=0.5, rely=0.8, anchor=CENTER)

                        # Display name of each item
                        globals()[tempnameL] = Label(frame, text=it[0], font=("", FontSizes[6], "bold"),
                                                     fg=self.allColors['black'][0], bg=self.allColors['itemframe'][0])
                        globals()[tempnameL].place(relx=0.5, rely=0.5, anchor=CENTER)
                        self.itemlabels.append(globals()[tempnameL])

                if isEmpty:
                    tempnameL = 'self.itemframe' + checkerStr + 'item'
                    tempnamePi = 'self.itemframe' + checkerStr + 'im'
                    tempnameP = 'self.itemframe' + checkerStr + 'add'
                    globals()[tempnamePi] = resizeImage('gui\\images\\rsz_add.jpg',
                                                        self.SectionLoc["addIm"][0],
                                                        self.SectionLoc["addIm"][1])

                    globals()[tempnameP] = Add_Button(frame, self.bodyframe1, self.window, i, globals()[tempnamePi],
                                                      self.allColors['bodyframe3'][0], self.Toolbox, self.varLevel)
                    globals()[tempnameP].place(relx=0.92, rely=0.88, anchor=CENTER)

                    globals()[tempnameL] = Label(frame, text="Empty", font=("", FontSizes[6], "bold"),
                                                 fg=self.allColors['black'][0], bg=self.allColors['itemframe'][0])
                    globals()[tempnameL].place(relx=0.5, rely=0.5, anchor=CENTER)
                    # self.itemlabels.append(globals()[tempnameL])

        ###Display Each Level
        self.currentLevel.trace('w', my_show)

        # Outstanding items to be returned - Create alert notification
        self.alertStatus = False
        for level in self.Toolbox.listLevels:
            if len(level.inUse) != 0:
                self.alertStatus = True
        if self.alertStatus:
            self.alertImage = Image.open('gui\\images\\alert.png')
            self.alertImageW, self.alertImageH = self.alertImage.size
            self.alertImage = self.alertImage.resize((SectionLoc["alert"][2], SectionLoc["alert"][3]))
            photo = ImageTk.PhotoImage(self.alertImage)
            self.alert = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
            self.alert.image = photo
            self.alert.place(x=SectionLoc["alert"][0], y=SectionLoc["alert"][1])
        else:
            self.alertImage = Image.open('gui\\images\\ok.jpg')
            self.alertImageW, self.alertImageH = self.alertImage.size
            self.alertImage = self.alertImage.resize((SectionLoc["alert"][2], SectionLoc["alert"][3]))
            photo = ImageTk.PhotoImage(self.alertImage)
            self.alert = Label(self.sidebar, image=photo, bg=self.allColors['white'][0])
            self.alert.image = photo
            self.alert.place(x=SectionLoc["alert"][0], y=SectionLoc["alert"][1])


def win():
    window = Tk()
    window.attributes('-fullscreen', True)
    Manager(window)
    window.mainloop()


if __name__ == '__main__':
    win()
