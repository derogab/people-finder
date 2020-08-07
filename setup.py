import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="people_finder",
    version="0.1.1-alpha",
    author="derogab",
    author_email="derosagabriele@outlook.it",
    description="A tool to recognize people in images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derogab/people_finder",
    license='MIT',
    package_dir={'people_finder': 'people_finder'},
    packages=[
        'people_finder',
    ],
    install_requires=[
        'uuid',
        'tinydb',
        'dlib',
        'face_recognition'
    ],
    keywords='people_finder',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)