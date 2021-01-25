from setuptools import setup, find_namespace_packages

setup(
    name="lootbot",
    version="0.1.0",
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'lootbot=lootbot.main:run'
        ]
    }
)
