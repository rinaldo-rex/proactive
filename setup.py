from setuptools import setup


setup(
    name='Proactive',
    version='1.0',
    py_modules=['proactive'],
    install_requires=[
        'Click',
        'Arrow'
        # TODO:'colorama' for using colors in windows
    ],
    entry_points='''
        [console_scripts]
        act=proactive:cli
    '''
)
