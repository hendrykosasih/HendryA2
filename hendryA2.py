from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
import string

LOWER=string.ascii_lowercase
UPPER=string.ascii_uppercase

class menu(App):
    status = StringProperty()

    def __init__(self):
        super(menu, self).__init__()
        itemLists ={}
        input_file = open("inventory.csv", "r")
        for items in input_file:
            items = items.strip().split(",")
            itemLists[items[0]]= [items[1], items[2], items[3]]
        self.mode = 1
        self.itemLists = itemLists
        self.status = "Choose action from the left menu, then select items on the right"

    def build(self):
        self.title = "Equipment Hire"
        self.root = Builder.load_file('popup.kv')
        self.create_entry_buttons()
        return self.root

    def create_entry_buttons(self):
        self.root.ids.itemsBox.clear_widgets()
        for key in self.itemLists:
            temp_button = Button(text=key)
            temp_button.bind(on_release=self.press_item)
            if self.itemLists[key][2] == 'out':
                temp_button.background_color = 1, 0, 0, 1
            if self.itemLists[key][2] == 'in':
                temp_button.background_color = 0, 1, 0, 1
            self.root.ids.itemsBox.add_widget(temp_button)

    def press_item(self, instance):
        name = instance.text
        if self.mode == 1:
            if self.itemLists[name][2] == 'in':
                self.status = "{} ({}), ${} is in".format(name, self.itemLists[name][0], self.itemLists[name][1])
            elif self.itemLists[name][2] == 'out':
                self.status = "{} ({}), ${} is out".format(name, self.itemLists[name][0], self.itemLists[name][1])
        elif self.mode == 2:
            if self.itemLists[name][2] == 'in':
                self.status = "Hiring {} for ${}".format(name, self.itemLists[name][1])
            elif self.itemLists[name][2] == 'out':
                self.status = "Hiring 0 item for $0.00"
        elif self.mode == 3:
            if self.itemLists[name][2] == 'out':
                self.status = "Returning {} ".format(name)
            elif self.itemLists[name][2] == 'in':
                self.status = "Returning 0 item"

    def add(self):
        self.status = "Enter details for new item"
        self.root.ids.popup.open()
        self.mode = 'list'

    def save(self, addedName , addedDesc, addedPrice):
        error_mode = 0
        check = 0
        try:
            finalPrice = float(addedPrice)
            if addedName == "" or addedDesc == "":
                error_mode = 1
                error = "Error"
                check = float(error)
                print(check)
            elif finalPrice < 0:
                error_mode = 2
                error = "Error"
                check = float(error)
            else:
                self.itemLists[addedName] = [addedDesc, addedPrice, 'in']
                temp_button = Button(text=addedName)
                temp_button.bind(on_release=self.press_item)
                temp_button.background_color = 0, 1, 0, 1
                self.root.ids.itemsBox.add_widget(temp_button)
                self.root.ids.popup.dismiss()
                self.clear_fields()
                self.status = "Choose action from the left menu, then select items on the right"
        except ValueError:
            if error_mode == 0:
                if addedName == "" or addedDesc == "" or addedPrice =="":
                    self.status = "All fields must be completed"
                else:
                    self.status = "Please enter a valid number"
            elif error_mode == 1:
                self.status = "All fields must be completed"
            elif error_mode == 2:
                self.status = "Price must not be negative"

    def clear_fields(self):
        self.root.ids.addedName.text = ""
        self.root.ids.addedDesc.text = ""
        self.root.ids.addedCost.text = ""

    def cancel(self):
        self.root.ids.popup.dismiss()
        self.clear_fields()
        self.status = "Choose action from the left menu, then select items on the right"

    def list(self):
        self.mode = 1
        self.status = "Select an item from the right menu to show it\'s description"

    def hire(self):
        self.create_entry_buttons()
        self.mode = 2
        self.status = "Select available items to hire"

    def return1(self):
        self.create_entry_buttons()
        self.mode = 3
        self.status = "Select available items to return"

    def confirm(self):
        for key in self.itemLists:
            if key in self.status and 'Hiring' in self.status:
                self.itemLists[key][2] = 'out'
            elif key in self.status and 'Returning' in self.status:
                self.itemLists[key][2] = 'in'
        self.create_entry_buttons()
        self.mode = 1
        self.status = "Choose action from the left menu, then select items on the right"

    def save_list(self):
        saving = []
        sortedlist = sorted(self.itemLists, key=self.itemLists.__getitem__)
        for key in sortedlist:
            temp = []
            temp.append(key)
            temp.append(self.itemLists[key][0])
            temp.append(self.itemLists[key][1])
            temp.append(self.itemLists[key][2])
            saving.append(temp)
        output_file = open("inventory.csv", "w")
        for each in saving:
            if each[3] == 'out':
                print("{},{},{},out".format(each[0], each[1], each[2]), file=output_file)
            elif each[3] == 'in':
                print("{},{},{},in".format(each[0], each[1], each[2]), file=output_file)
        print("{} items have been saved to inventory.csv".format(len(saving)))
        output_file.close()

menu().run()

