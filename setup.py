import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="people-finder",
    version="0.2.4-beta",
    author="derogab",
    author_email="derosagabriele@outlook.it",
    description="A tool to recognize people in images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derogab/people-finder",
    license='MIT',
    package_dir={'people_finder': 'people_finder'},
    packages=[
        'people_finder',
    ],
    install_requires=[
        'uuid',
        'numpy',
        'scikit-learn',
        'opencv-python',
        'face_recognition'
    ],
    keywords='people-finder',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)