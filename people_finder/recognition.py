import os
import face_recognition
from people_finder.database import Database

class Recognition:

    def __init__(self):
        ''' Constructor for Recognition class. '''
        pass

    def __in_array(self, item, array):
        ''' Check if item is in array. '''
        for i in array:
            if item == i:
                return True
        return False

    def __array_bool(self, array):
        ''' Check if a value is true in array. '''
        for value in array:
            if value == True:
                return True
        return False

    def __insert_person(self, person):
        ''' Insert person in db. '''
        self.db.insert_person(person)

    def set_database(self, db_file):
        ''' Set db file to use. '''
        self.db = Database(db_file)

    def insert_recognizable_people(self, recognizable_people):
        ''' Insert recognizable people. '''
        for person in recognizable_people:
            self.__insert_person(person)

    def find_people_in_image(self, filename):
        ''' Find people in a image. '''
        people_found = []

        # Load the jpg file into numpy array
        unknown_image = face_recognition.load_image_file(filename)
        
        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        unknown_face_locations = face_recognition.face_locations(unknown_image, model="hog")
        
        # Check if there are people
        if len(unknown_face_locations) == 0:
            # No people detected
            return []

        # Check image for each known person
        for person in self.db.get_people():
            person_known_faces = []

            for file in os.listdir(person.get_source()):
                if file.endswith(".jpg"):

                    # Load the jpg file into numpy array
                    person_image = face_recognition.load_image_file(os.path.join(person.get_source(), file))

                    # Get the face encodings for each face in each image file
                    # Since there could be more than one face in each image, it returns a list of encodings.
                    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
                    try:
                        person_face_encoding = face_recognition.face_encodings(person_image)[0]
                    except IndexError:
                        # I wasn't able to locate any faces in at least one of the images. Check the image files.
                        continue
                    
                    # Insert encoded face in list
                    person_known_faces.append(person_face_encoding)

            if person_known_faces != []:

                for unknown_face_location in unknown_face_locations:

                    # Print the location of each face in this image
                    top, right, bottom, left = unknown_face_location

                    # You can access the actual face itself like this:
                    face_image = unknown_image[top:bottom, left:right]

                    # Encode found image
                    try:
                        unknown_face_encoding = face_recognition.face_encodings(face_image)[0]
                    except IndexError:
                        # I wasn't able to locate any faces in at least one of the images. Check the image files.
                        continue

                    # results is an array of True/False telling if the unknown face matched anyone in the person_known_faces array
                    results = face_recognition.compare_faces(person_known_faces, unknown_face_encoding)

                    if self.__array_bool(results):
                        # This person is in the image
                        if not self.__in_array(person, people_found): # check if found previously
                            people_found.append(person)

        return people_found