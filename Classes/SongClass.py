# Song class, fields: name, info , indexName, path
class Song:
    # constructor.
    def __init__(self, songName, information, indexNumber, pathdest):
        self.name = songName
        self.info = information
        self.indexName = indexNumber
        self.path = pathdest

    # getters
    def getInfo(self):
        return self.info

    def getName(self):
        return self.name

    def getIndexName(self):
        return self.indexName

    def getPath(self):
        return self.path


