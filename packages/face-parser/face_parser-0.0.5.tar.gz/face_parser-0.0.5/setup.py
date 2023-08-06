import setuptools

setuptools.setup(
        name="face_parser",
        version="0.0.5",
        author="Ross Leitch",
        author_email="ross@end-game.com",
        description="A small package to turn dlib's facial landmarks into more interesting values",
        url="https://github.com/balbatross/dlib-face-parser",
        packages=['face_parser'],
        install_requires=[
            'scipy',
            'numpy',
            'imutils'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
)
