# people-finder
A tool to easy recognize people in images.

### Install
```
pip install people-finder
```

### Usage
```python
from people_finder import Recognition

# Init
r = Recognition()

# Insert recognizable people
p1 = 'P1'
p2 = 'P2'
r.insert_recognizable_people([p1, p2], train_folder_path = 'path/to/known/people')

# Train the dataset
r.train_dataset(train_folder_path = 'path/to/known/people', trained_model_path = "trained_model.clf")

# Find people in an image
res = r.find_people_in_image('/path/to/image.jpg', trained_model_path = "trained_model.clf")
print('People found:')
for person in res:
    print(person)
```