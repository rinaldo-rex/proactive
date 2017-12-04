from setuptools import setup


setup(
    name='Proactive',
    version='1.0',
    py_modules=['proactive'],
    install_requires=[
        'Click',
        'Arrow',
        'backports.functools_lru_cache'
        # TODO:'colorama' for using colors in windows
    ],
    entry_points='''
        [console_scripts]
        act=proactive:cli
    '''
)
