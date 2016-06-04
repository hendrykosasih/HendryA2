"""
Hendry
05 June 2016
This program loads and reads csv file when loaded. Users can list all of the available and out of stock items, hire
items and return items by confirming their decision, add new list of items, and, finally, save the changes which affects
the csv file. Users can only hire or return an item at once for every confirmation. The items highlighted in green are
available, while the items highlighted in red are out of stock.
Github URL : https://github.com/hendrykosasih/HendryA2.git
"""


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
import string

class menu(App):    #defining base class of kivy app
    status = StringProperty()   #all string are treated as ASCII

    def __init__(self):     #constructor of clasess
        super(menu, self).__init__()
        itemLists ={}   #place(dictionary) to store item lists
        input_file = open("inventory.csv", "r")     #Open and read the csv file
        for items in input_file:
            items = items.strip().split(",")    #split the data with "," as the indentation
            itemLists[items[0]]= [items[1], items[2], items[3]]     #assigned keyword for each item
        self.mode = 1
        self.itemLists = itemLists      #assigned self.itemLists to itemLists variable
        self.status = "Choose action from the left menu, then select items on the right"    #show the current situation

    def build(self):
        self.title = "Equipment Hire"   #app title
        self.root = Builder.load_file('popup.kv')   #connect with the kivy file
        self.create_entry_buttons()     #to create entry buttons
        return self.root    #return value to root

    def create_entry_buttons(self):
        """This function sets the items button and background color"""
        self.root.ids.itemsBox.clear_widgets()
        for key in self.itemLists:
            temp_button = Button(text=key)
            temp_button.bind(on_release=self.press_item)    #action of pressing item button
            if self.itemLists[key][2] == 'out':     #background highlighted in red color for unavailable item
                temp_button.background_color = 1, 0, 0, 1   #red background
            if self.itemLists[key][2] == 'in':      #background highlighted in green color for available item
                temp_button.background_color = 0, 1, 0, 1   #green background
            self.root.ids.itemsBox.add_widget(temp_button)

    def press_item(self, instance):
        """This function gives action when item button pressed"""
        name = instance.text
        """Divided into several parts"""
        if self.mode == 1:  #show the description of items when the button is clicked
            if self.itemLists[name][2] == 'in': #item is available
                self.status = "{} ({}), ${} is in".format(name, self.itemLists[name][0], self.itemLists[name][1])
            elif self.itemLists[name][2] == 'out':  #item is not available
                self.status = "{} ({}), ${} is out".format(name, self.itemLists[name][0], self.itemLists[name][1])
        elif self.mode == 2:    #for the hiring section
            if self.itemLists[name][2] == 'in':     #hiring an available item
                self.status = "Hiring {} for ${}".format(name, self.itemLists[name][1])     #show the chosen item and it's description
            elif self.itemLists[name][2] == 'out':  #hiring an unavailable item
                self.status = "Hiring 0 item for $0.00"     #because of unavailable item, 0 item is selected
        elif self.mode == 3:    #for the returning section
            if self.itemLists[name][2] == 'out':    #returning an hired item
                self.status = "Returning {} ".format(name)  #return item successfull and show returned name of item
            elif self.itemLists[name][2] == 'in':   #returning an not hired item
                self.status = "Returning 0 item"    #because item is not hired, there is nothing to be returned

    def add(self):
        """This function is to add new item to the app"""
        self.status = "Enter details for new item"  #ask user to enter new item details
        self.root.ids.popup.open()      #a popup menu will be open
        self.mode = 'list'

    def save(self, addedName , addedDesc, addedPrice):
        """This function checks the integrity of the details of the new item added"""
        error_mode = 0
        check = 0
        try:
            finalPrice = float(addedPrice)
            if addedName == "" or addedDesc == "":  #check whether fields are filled
                error_mode = 1
                error = "Error"
                check = float(error)
                print(check)
            elif finalPrice < 0:    #check whether price is not under 0
                error_mode = 2
                error = "Error"
                check = float(error)
            else:
                self.itemLists[addedName] = [addedDesc, addedPrice, 'in']       #description of new added item
                temp_button = Button(text=addedName)    #button available for this new added item
                temp_button.bind(on_release=self.press_item)
                temp_button.background_color = 0, 1, 0, 1       #set the background color of the new added item
                self.root.ids.itemsBox.add_widget(temp_button)
                self.root.ids.popup.dismiss()   #close the popup menu after creating new item
                self.clear_fields()     #call clear fields function
                self.status = "Choose action from the left menu, then select items on the right"
        except ValueError:
            if error_mode == 0:     #error because of the empty fields
                if addedName == "" or addedDesc == "" or addedPrice =="":
                    self.status = "All fields must be completed"       #error message that prompt user to complete all fields
                else:
                    self.status = "Please enter a valid number"     #error because of invalid price and prompt user to enter valid number
            elif error_mode == 1:   #error because of empty fields
                self.status = "All fields must be completed"  # error message that prompt user to complete all fields
            elif error_mode == 2:   #error because of negative price
                self.status = "Price must not be negative"  #ask user to enter positive price

    def clear_fields(self):
        """This function is to clear all of the add new item menu fields"""
        self.root.ids.addedName.text = ""   #clear the item name field
        self.root.ids.addedDesc.text = ""   #clear the item description field
        self.root.ids.addedCost.text = ""   #clear the item price field

    def cancel(self):
        """This function is to dismiss and close the add new item menu and clear all of the fields inputs."""
        self.root.ids.popup.dismiss()   #user clicks cancel button
        self.clear_fields()     #call clear fields function
        self.status = "Choose action from the left menu, then select items on the right"

    def list(self):
        """List the all items when user clicks list button"""
        self.mode = 1
        self.status = "Select an item from the right menu to show it\'s description"

    def hire(self):
        """Show the user which items are available and unavailable to hire"""
        self.create_entry_buttons()     #call create entry buttons function
        self.mode = 2
        self.status = "Select available items to hire"  #show action message

    def return1(self):
        """Show the user which items are available and unavailable to return"""
        self.create_entry_buttons()     #call create entry buttons function
        self.mode = 3
        self.status = "Select available items to return"    #show action message

    def confirm(self):
        """This function is to confirm the user's selection for hire and return"""
        for key in self.itemLists:
            if key in self.status and 'Hiring' in self.status:
                self.itemLists[key][2] = 'out'
            elif key in self.status and 'Returning' in self.status:
                self.itemLists[key][2] = 'in'
        self.create_entry_buttons()  # call create entry buttons function
        self.mode = 1
        self.status = "Choose action from the left menu, then select items on the right"    #show action message

    def save_list(self):
        """This function is to save the changes of the data and write it on csv file"""
        saving = []     #create list for number of item
        sortedlist = sorted(self.itemLists, key=self.itemLists.__getitem__)     #sort list
        for key in sortedlist:
            temp = []   #create list for item list
            temp.append(key)    #add key to temp variable
            temp.append(self.itemLists[key][0])
            temp.append(self.itemLists[key][1])
            temp.append(self.itemLists[key][2])
            saving.append(temp)     #add temp to saving list
        output_file = open("inventory.csv", "w")    #open csv file and write data on it
        for each in saving:
            if each[3] == 'out':    #item out
                print("{},{},{},out".format(each[0], each[1], each[2]), file=output_file)
            elif each[3] == 'in':   #item in
                print("{},{},{},in".format(each[0], each[1], each[2]), file=output_file)
        print("{} items have been saved to inventory.csv".format(len(saving)))  #show user how many items saved to inventory
        output_file.close()     #close the file

menu().run()
#end of program
