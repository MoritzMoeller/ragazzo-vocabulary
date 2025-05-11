from setuptools import setup

setup(
    name="ragazzo-vocabulary",
    version="0.1.0",
    description="Tool to export Anki flashcards to GitHub Pages",
    author="Moritz Möller",
    author_email="moritz.moeller.home@gmail.com",
    py_modules=["anki_fetcher"],
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ragazzo-vocabulary=anki_fetcher:main",
        ],
    },
)
