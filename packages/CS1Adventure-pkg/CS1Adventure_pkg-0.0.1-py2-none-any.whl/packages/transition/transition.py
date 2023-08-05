

class transition:

    def __init__(self, name, area, direction, destination , isPassable, description):
        self.name = name
        self.area = area
        self.direction = direction
        self.destination = destination
        self.isPassable = isPassable
        self.onSuccess = None
        self.onFailure = None
        self.description = description
        self.onSuccessScripts = []
        self.onFailureScripts = []

    def printTrans(self):
        print( "You see a " + self.name + ". " + self.description + " It seems to lead "+ self.direction)
