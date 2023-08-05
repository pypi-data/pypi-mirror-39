from setuptools import setup


setup(
    
    name                = 'dj-shortnr',
    version             = '0.1.0',
    description         = 'Yet another django app for URL indexing and shortening',
    long_description    = 'README in GitHub',
    url                 = 'http://github.com/dsfx3d/dj-shortnr',
    author              = 'dsfx3d',
    author_email        = 'dsfx3d@gmail.com',
    license             = 'MIT',
    packages            = ['shortnr'],
    zip_safe            = False,
    include_package_data= True,

    keywords            = 'django app url shortening indexing',
    classifiers         = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ]

)