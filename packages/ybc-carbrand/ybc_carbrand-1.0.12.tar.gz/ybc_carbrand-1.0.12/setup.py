from distutils.core import setup

setup(
    name='ybc_carbrand',
    version='1.0.12',
    description='Get all car brands',
    long_description='Get all car brands from carbrands.json',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'carbrand', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_carbrand'],
    package_data={'ybc_carbrand': ['data/*', '*.py']},
    license='MIT',
    install_requires=['ybc_exception']
)
