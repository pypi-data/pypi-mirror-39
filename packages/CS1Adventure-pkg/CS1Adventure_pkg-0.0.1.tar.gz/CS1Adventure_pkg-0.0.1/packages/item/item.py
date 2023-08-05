class item:

    def __init__(self, name, description, area, moveable):
        self.name = name
        self.description = description
        self.area = area
        self.moveable = moveable
        self.onSuccess = None
        self.onFailure = None
        self.onSuccessScripts = []
        self.onFailureScripts = []


    def printItem(self):
        print( "You see a " + self.name + ". " + self.description)
