from setuptools import setup

setup(
    name="mbroker",
    version='0.1',
    py_modules=['broker'],
    install_requires=[
        'Click',
    ],
    python_requires='>=3.10',
    entry_points='''
        [console_scripts]
        mbroker=broker:cli
    ''',
)
