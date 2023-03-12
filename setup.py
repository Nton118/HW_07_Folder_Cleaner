from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()


setup(
    name='clean_folder_util',
    version='0.0.6',
    description='Utility to sort files inside the specified folder',
    long_description=long_desc,
    author='Anton Petrenko',
    author_email='anton.drumma@gmail.com',
    url='https://github.com/Nton118/FolderCleaner.git',
    license='MIT',
    packages=find_packages(),
    data_files=[('Clean_folder', ['Clean_folder/config.txt'])],
    entry_points={'console_scripts': ['clean_folder = Clean_folder.clean:main']},
    include_package_data=True
) 