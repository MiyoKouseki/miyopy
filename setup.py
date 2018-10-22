from setuptools import setup


requires = ["requests>=2.14.2"]


setup(
    name='miyopy',
    version='0.1',
    description='Awesome library',
    url='https://github.com/MiyoKouseki/miyopy.git',
    author='MiyoKouseki',
    author_email='miyo@icrr.u-tokyo.ac.jp',
    license='MIT',
    keywords='sample setuptools development',
    #packages=[
    #    "your_package",
    #    "your_package.subpackage",
    #],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
