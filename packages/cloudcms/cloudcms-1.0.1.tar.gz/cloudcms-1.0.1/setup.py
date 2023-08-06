import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cloudcms',
    version='1.0.1',
    author='Michael Whitman',
    author_email='michael.whitman@cloudcms.com',
    description='Cloud CMS Python Driver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitana/cloudcms-python-driver',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
)