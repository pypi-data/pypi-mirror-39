from packages.item.item import item
from packages.area.area import Area


class player:


    def __init__(self, name="Player", description="",inventory=[]):
        self.description = description
        self.currentArea = None;
        self.name = name
        self.inventory = inventory


    def printPlayer(self):
        print "You are " + self.name + ". " + self.description

    def addToInventory(self, targetItem):
        area1 = self.currentArea
        itemObj = None
        for item in area1.items:
            if targetItem == item.name:

                if item.moveable == True:
                    itemObj = item

                    self.inventory.append(item)
                    if item.onSuccess == None:
                        print("You picked up the " + targetItem)
                    else:
                        print(item.onSuccess)
                    area1.removeItem(item)
                else:
                    if item.onFailure == None:
                        print("You cannot take the " + targetItem)
                    else:
                        print(item.onFailure)
                return

        print "There is no " + targetItem

    def dropFromInventory(self, item):
        item.area = self.currentArea
        self.inventory.remove(item)

    def printInventory(self):
        if len(self.inventory) != 0:
            for item in self.inventory:
                print(item.name + " - " + item.description)
        else:
            print "[Empty]"
