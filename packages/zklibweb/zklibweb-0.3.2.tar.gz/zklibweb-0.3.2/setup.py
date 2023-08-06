from setuptools import setup


def requirements():
    req = []
    for line in open('requirements/base.txt', 'r'):
        req.append(line)
    return req

setup(
    name='zklibweb',
    version='0.3.2',
    description='Library for read data from zklib maquines, using selenium and requests',
    long_description=open('readme.rst').read(),
    url='http://github.com/franzemil/zklibweb',
    author='Franz Emil Eulate Chacolla',
    author_email='franzemil35@gmail.com',
    license='MIT',
    packages=['zklibweb'],
    keywords='zklib web mopsv',
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    install_requires=requirements(),
    zip_safe=False
)
