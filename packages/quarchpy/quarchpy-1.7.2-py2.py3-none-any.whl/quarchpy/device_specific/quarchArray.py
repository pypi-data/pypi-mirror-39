from device import quarchDevice

class quarchArray(quarchDevice):
    def __init__(self, originObj):
        self.originObj = originObj
        self.connectionObj = originObj.connectionObj
        self.ConType = originObj.ConType

    def getSubDevice(self, port):
        return subDevice(self.originObj, port)

class subDevice(quarchArray):

    def __init__(self, originObj, port):
        self.port = port
        self.originObj = originObj
        self.connectionObj = originObj.connectionObj
        self.ConType = originObj.ConType

    def sendCommand(self, CommandString):
        return repr(self.originObj.sendCommand(CommandString + " <" + str(self.port) + ">")).replace("\\r\\n"+ str(self.port) + ":", "\r\n").replace("'"+ str(self.port) +":", "").replace("'", "").replace("uFa", "Fa")