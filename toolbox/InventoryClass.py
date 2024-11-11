import json
from tkinter import *
from PIL import Image, ImageTk
from toolbox.InventoryClass import *
import csv
from datetime import datetime
import glob


class Level:
    def __init__(self, name):
        self.name = name
        self.empty = [1, 2, 3, 4, 5, 6, 7, 8]
        self.inUse = []
        self.available = []
        self.items = []

    def add_items(self, items):
        for item in items:
            if len(self.empty) != 0:
                self.items.append(Item(item, self.empty[0]))
                self.available.append(item)
                self.empty = self.empty[1:]

    def get_items(self):
        listToBeReturned = []
        for item in self.items:
            tempList = [item.name, item.position, item.status, item.user, item.condition]
            listToBeReturned.append(tempList)
        return listToBeReturned

    def use_item(self, name, user, date):
        for i in self.items:
            if name == i.name:
                i.status = 'In Use'
                i.user = user
                i.date = date
                self.inUse.append(name)
                try:
                    self.available.remove(name)
                except:
                    print('initialising')

    def ret_item(self, name, date):
        for i in self.items:
            if name == i.name:
                i.status = 'Available'
                i.user = 'Not in Use'
                i.date = date
                self.inUse.remove(name)
                self.available.append(name)

    def load_items(self, name, item):
        self.temp = int(item['Position'][-1])
        a = Item(name, self.temp)
        a.status = item['Status']
        a.user = item['User']
        a.condition = item['Condition']
        a.date = item['Date']
        self.items.append(a)

    def item_user(self, name):
        for i in self.items:
            if name == i.name:
                return i.user


class Item:
    def __init__(self, name, pos):
        self.name = name
        self.position = 'Position ' + str(pos)
        self.status = 'Available'
        self.user = 'Not in Use'
        self.condition = 'Working'
        self.date = ''


class Toolbox:
    def __init__(self):
        self.AllLevels = ToolboxInv

        self.Level1 = Level('Level 1')
        self.Level1.add_items(self.AllLevels['Level1'])

        self.Level2 = Level('Level 2')
        self.Level2.add_items(self.AllLevels['Level2'])

        self.Level3 = Level('Level 3')
        self.Level3.add_items(self.AllLevels['Level3'])

        self.Level4 = Level('Level 4')
        self.Level4.add_items(self.AllLevels['Level4'])

        self.Level5 = Level('Level 5')
        self.Level5.add_items(self.AllLevels['Level5'])

        self.Level6 = Level('Level 6')
        self.Level6.add_items(self.AllLevels['Level6'])

        self.Level7 = Level('Level 7')
        self.Level7.add_items(self.AllLevels['Level7'])

        self.listLevels = [self.Level1, self.Level2, self.Level3, self.Level4, self.Level5, self.Level6, self.Level7]
        self.records = []
        try:
            filesR = glob.glob("load/*.csv")
            filesR.sort(reverse=True)
            with open(filesR[0], newline='') as f:
                reader = csv.reader(f)
                self.records = list(reader)
        except:
            print("Error reading csv file. Initialising empty records.")

    def retrieve_level(self, string):
        key = int(string) - 1
        return self.listLevels[key]

    def save_log(self):
        log = {}
        for level in self.listLevels:
            log[level.name] = {}
            log[level.name]["items"] = {}
            log[level.name]['Empty'] = level.empty
            log[level.name]['In Use'] = level.inUse
            log[level.name]['Available'] = level.available
            for item in level.items:
                log[level.name]["items"][item.name] = {}
                log[level.name]["items"][item.name]["Position"] = item.position
                log[level.name]["items"][item.name]["Status"] = item.status
                log[level.name]["items"][item.name]["User"] = item.user
                log[level.name]["items"][item.name]["Condition"] = item.condition
                log[level.name]["items"][item.name]["Date"] = item.date
        save_inv_file = "load/inventory-" + str(datetime.now())[:10] + ".json"
        save_rec_file = "load/records-" + str(datetime.now())[:10] + ".csv"
        with open(save_inv_file, "w") as write_file:
            json.dump(log, write_file)

        with open(save_rec_file, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerows(self.records)
        print('file saved')

    def load_log(self):
        filesI = glob.glob("load/*.json")
        filesI.sort(reverse=True)
        with open(filesI[0], 'r') as file:
            data = json.load(file)
        for i in range(7):
            level = "Level " + str(i + 1)
            self.listLevels[i].empty = data[level]["Empty"]
            self.listLevels[i].inUse = data[level]["In Use"]
            self.listLevels[i].available = data[level]["Available"]
            self.listLevels[i].items = []
            itemss = list(data[level]['items'].keys())
            for j in itemss:
                self.listLevels[i].load_items(j, data[level]['items'][j])
        print('file loaded')

    def add_records(self, user, device, level, status, date):
        self.recToAdd = [user, device, level, status, date]
        self.records.insert(0, self.recToAdd)

        # Save into file
        save_rec_file = "load/records-" + str(datetime.now())[:10] + ".csv"
        with open(save_rec_file, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerows(self.records)


# Function to retrieve details from each level
def getItemDetails(items):
    listToBeReturned = []
    for item in items:
        tempList = [item.name, item.position, item.status, item.user, item.condition]
        listToBeReturned.append(tempList)
    return listToBeReturned


def resizeImage(dir, a, b):
    im = Image.open(dir)
    ImageW, ImageH = im.size
    imm = im.resize((a, b))
    photo = ImageTk.PhotoImage(imm)
    return photo


# Import Data from source
ToolboxInv = {}
ToolboxInv['Level1'] = ['Item 1']
ToolboxInv['Level2'] = []
ToolboxInv['Level3'] = ['Mallet (Wood)', "3/4\" Chisel", "2\" Chisel", "1 1/2\" Chisel", '24 oz Mallet',
                        '9 Pc Hex Key Set', '7 Pc Screwdriver Set', 'T-Bar']
ToolboxInv['Level4'] = []
ToolboxInv['Level5'] = []
ToolboxInv['Level6'] = []
ToolboxInv['Level7'] = []
