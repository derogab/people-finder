from tinydb import TinyDB, Query
from people_finder.person import Person

class Database:
    
    def __init__(self, db_path):
        ''' Constructor for Database class. '''
        self.db = TinyDB(db_path)

    def get_people(self):
        ''' Get all people in database. '''
        people = []
        people_data = self.db.table('people').all()

        for person_data in people_data:

            name = person_data['name']
            source = person_data['source']

            people.append(Person(name, source))
        
        return people
        
    def insert_person(self, person):
        ''' Insert a new person in database. '''
        self.db.table('people').insert(person.get())
