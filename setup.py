from setuptools import setup


setup(
    name='Proactive',
    version='0.1',
    py_modules=['proactive'],
    install_requires=[
        'Click',
        # TODO:'colorama' for using colors in windows
    ],
    entry_points='''
        [console_scripts]
        act=proactive:cli
    '''
)
