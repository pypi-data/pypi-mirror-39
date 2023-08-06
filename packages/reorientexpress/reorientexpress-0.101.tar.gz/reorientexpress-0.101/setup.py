import setuptools

setuptools.setup(
    name = 'reorientexpress',
    version = '0.101',
    scripts = ['reorientexpress.py'],
    author = 'Angel Ruiz Reche',
    author_email = 'angelrure@gmail.com',
    description = 'Script used to build, test and use models that predict the orientation of cDNA reads',
    url = 'https://github.com/angelrure/reorientexpress',
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3"
    ]
)