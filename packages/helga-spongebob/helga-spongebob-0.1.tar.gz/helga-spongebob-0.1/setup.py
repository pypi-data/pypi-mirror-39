from setuptools import setup, find_packages

version = '0.1'

setup(
    name="helga-spongebob",
    version=version,
    description=('HeLgA PlUgIn tO Do mOcKiNg sPoNgEbOb tExT'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Framework :: Twisted',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='helga spongebob',
    author='Shaun Duncan',
    author_email='shaun.duncan@gmail.com',
    url='https://github.com/shaunduncan/helga-spongebob',
    license='MIT',
    packages=find_packages(),
    py_modules=['helga_spongebob'],
    entry_points=dict(
        helga_plugins=[
            'spongebob = helga_spongebob:spongebob'
        ],
    ),
)
