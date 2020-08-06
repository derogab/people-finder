import uuid

class Person:
    
    def __init__(self, name, source):
        ''' Constructor for Person class. '''
        self.id     = self.__generate_id()
        self.name   = name
        self.source = source

    def __generate_id(self):
        ''' Generate unique id. '''
        return uuid.uuid1().hex

    def get(self):
        ''' Get all data in a dictionary. '''
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source
        }

    def get_id(self):
        ''' Get the unique id. '''
        return self.id

    def get_name(self):
        ''' Get the name. '''
        return self.name

    def get_source(self):
        ''' Get the path of images. '''
        return self.source
