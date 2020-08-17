import math
from sklearn import neighbors
import os
import os.path
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import json
import uuid

class Recognition:

    def __init__(self, model='hog'):
        ''' Constructor for Recognition class. '''
        # Get deep learning face detection model 
        self.model = model
        if self.model not in ['hog', 'cnn']:
            self.model = 'hog'

    def __insert_person(self, name, known_people_path):
        ''' Insert person in known people folder. '''
        # Generate id
        id = uuid.uuid1().hex
        # Generate person
        person = {
            'id': id,
            'name': name
        }
        # Create person dir
        person_dir = os.path.join(known_people_path, 'id_' + id)
        os.mkdir(person_dir)
        # Write person in json file
        with open(os.path.join(person_dir, 'info.json'), 'w') as outfile:
            json.dump(person, outfile)

    def __train(self, train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree'):
        """
        Trains a k-nearest neighbors classifier for face recognition.

        :param train_dir: directory that contains a sub-directory for each known person.

        Structure:
            <train_dir>/
            ├── <person1>/
            │   ├── info.json
            │   ├── <somename1>.jpeg
            │   ├── <somename2>.jpeg
            │   ├── ...
            ├── <person2>/
            │   ├── info.json
            │   ├── <somename1>.jpeg
            │   └── <somename2>.jpeg
            └── ...

        :param model_save_path: (optional) path to save model on disk
        :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
        :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
        :return: returns knn classifier that was trained on the given data.
        """
        X = []
        y = []

        # Loop through each person in the training set
        for class_dir in os.listdir(train_dir):
            # Check if current person path is a dir
            if not os.path.isdir(os.path.join(train_dir, class_dir)):
                continue
            
            # Check if there is current person info file
            if not os.path.isfile(os.path.join(os.path.join(train_dir, class_dir), 'info.json')):
                continue
            with open(os.path.join(os.path.join(train_dir, class_dir), 'info.json')) as json_file:
                data = json.load(json_file)
            if not data or data['name'] == '':
                continue

            # Loop through each training image for the current person
            for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image, model=self.model)

                if len(face_bounding_boxes) == 1: # If there is 1 person in a training image
                    # Add face encoding for current image to the training set
                    X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    y.append(data['name'])

        # Determine how many neighbors to use for weighting in the KNN classifier
        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(X))))

        # Create and train the KNN classifier
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
        knn_clf.fit(X, y)

        # Save the trained KNN classifier
        if model_save_path is not None:
            with open(model_save_path, 'wb') as f:
                pickle.dump(knn_clf, f)

        return knn_clf

    def __predict(self, X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
        """
        Recognizes faces in given image using a trained KNN classifier

        :param X_frame: frame to do the prediction on.
        :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
        :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
        :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
            of mis-classifying an unknown person as a known one.
        :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """
        if knn_clf is None and model_path is None:
            raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:
                knn_clf = pickle.load(f)

        X_face_locations = face_recognition.face_locations(X_frame, model=self.model)

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []

        # Find encodings for faces in the test image
        faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    def insert_recognizable_people(self, people, train_folder_path = 'train/'):
        ''' Insert recognizable people. '''
        for person in people:
            self.__insert_person(person, train_folder_path)

    def train_dataset(self, train_folder_path = 'train/', trained_model_path = "trained_model.clf"):
        ''' Train known people '''
        return self.__train(train_folder_path, model_save_path=trained_model_path, n_neighbors=2)

    def find_people_in_image(self, filename, trained_model_path = "trained_model.clf"):
        ''' Find people in a image. '''
        # Load the jpg file into numpy array
        unknown_image = face_recognition.load_image_file(filename)
        # Find people in image
        predictions = self.__predict(unknown_image, model_path=trained_model_path)
        # Return the predictions
        return [person_found for person_found, location in predictions]