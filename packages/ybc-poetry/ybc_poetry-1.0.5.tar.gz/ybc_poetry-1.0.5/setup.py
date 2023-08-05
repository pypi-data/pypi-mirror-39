from distutils.core import setup

setup(
    name='ybc_poetry',
    version='1.0.5',
    description='Poetry search',
    long_description='Poetry search by title and author',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'python3', 'python', 'Poetry search'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_poetry'],
    package_data={'ybc_poetry': ['*.py']},
    license='MIT',
    install_requires=[
        'requests',
        'ybc_config',
        'ybc_exception'
    ]
)
