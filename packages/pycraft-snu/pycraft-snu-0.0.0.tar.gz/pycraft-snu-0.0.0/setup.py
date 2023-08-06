import setuptools

with open('README.md', 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name='pycraft-snu',
    version='0.0.0',
    author='The Pycraft Team @ SNUGifted \'18',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/minecraft-codingmath/pycraft',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyglet==1.3.2',
        'Deprecated==1.2.0',
        'msgpack_python==0.5.6',
        'pyzmq==17.1.2'
    ],
    project_urls={
        'Source': 'https://github.com/minecraft-codingmath/pycraft',
        'Bug Reports': 'https://github.com/minecraft-codingmath/pycraft/issues'
    },
    entry_points={
        'console_scripts': [
            'pycraft=pycraft:main'
        ]
    },
    package_data={
        'pycraft': ['texture.png']
    }
)
