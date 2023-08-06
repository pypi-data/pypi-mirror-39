from setuptools import setup

setup(
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'spellchecker = mlmorph_spellchecker.__main__:main'
        ],
    }
)
