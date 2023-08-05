
from codecs import open

from setuptools import setup




REQUIREMENTS = [
    'webob>=1.2.0',
    'six>=1.10.0'
]

EXTRA_REQUIREMENTS = {
    'jinja2>=2.4',
    'Babel>=2.2',
    'pytz>=2015.7'
}

setup(
    name='amanwa32',
    version='1.0.8',
    license='Apache Software License',
    description="testing wa3 custom",
    long_description='LONG_DESCRIPTION',
    author='a',
    author_email='angrish_aman@yahoo.com',
    zip_safe=False,
    platforms='any',
    py_modules=[
        'amanwa32',
    ],
    packages=[
        'amanwa32',
        'amanwa32_extras',

    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require={'extras': EXTRA_REQUIREMENTS},
    classifiers=[
       
    ]
)
