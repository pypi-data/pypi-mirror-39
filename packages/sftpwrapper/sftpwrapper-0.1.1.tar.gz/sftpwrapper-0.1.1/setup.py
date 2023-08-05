from setuptools import setup


def readme():
    with open('README.rst') as file:
        return file.read()


setup(
    name='sftpwrapper',
    version='0.1.1',
    license='MIT',
    author='Kyle Wolfe',
    author_email='kwolfe@northampton.edu',
    install_requires=['paramiko'],
    packages=[
        'sftpwrapper'
    ],
    url='',
    description='A python program that facilitates uploading and downloading of files to/from an SFTP server',
    long_description=readme(),
    include_package_data=True,
    keywords='sftp ftp',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ],
)
