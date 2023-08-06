import setuptools

requirements = [
    'translate',
    'click',
    'click-log',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="opml-translate",
    version='0.1.0',

    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'opml-trans=opml_translate.command_line:translate_command'
        ],
    },

    author="Daniel Pechersky",
    author_email='danny.pechersky@gmail.com',
    description="Translates OPML files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DanielPechersky/opml-translate',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)