from packages.item.item import item

class Area:


    def __init__(self,name, description = "A vast land of wonders, maybe I should take a look around?"):
        self.name = name
        self.transitions = []
        self.description = description
        self.items = []
        self.inAreaScripts = []



    def setDescription(self, description =""):
        self.description = description


    #Adds transition to the list of transitions
    def newTransition(self, transition):
        self.transitions.append(transition)

    def newItem(self, item):
        self.items.append(item)

    def printArea(self):
        print("You are in the " +self.name + ". " + self.description)

        for transition in self.transitions:
            transition.printTrans()
        for item in self.items:
            item.printItem()

    def removeItem(self, item):
        item.area = None
        self.items.remove(item)
