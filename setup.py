from setuptools import setup

setup(
    name='Boston Python Skill',
    version='1.0',
    description='Boston Python Alexa Skill',
    author='Michael Milkin',
    author_email='mmilkin@gmail.net',
    py_modules=['bp_alexa_skill'],
    install_requires=[
        'certifi',
        'chardet',
        'idna',
        'requests',
        'urllib3'
    ],
    classifiers=[
        'Topic :: Alexa :: Skill'
    ]
)
