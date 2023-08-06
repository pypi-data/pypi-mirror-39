from setuptools import setup, find_packages

__version__ = "0.0.0"


setup(
    name='doodads',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    author='Tyler Fisher',
    author_email='podgeracer9000@gmail.com',
    url='https://github.com/bp256r1/doodads',
    description='A hodgepodge of wild and exciting doodads',
    description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ],
)
