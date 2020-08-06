# people_finder
A tool to easy recognize people in images.

### Install
```
pip install people-finder
```

### Usage
```python
from people_finder import Recognition, Person

r = Recognition()
# Set the database 
r.set_database('/path/to/db.json')

# Insert recognizable people
p1 = Person('P1', '/path/to/p1/images/')
p2 = Person('P2', '/path/to/p2/images/')
r.insert_recognizable_people([p1, p2])

# Find people in an image
res = r.find_people_in_image('/path/to/image.jpg')
print('People found:')
for person in res:
    print(person.get_name())

```