import os

from setuptools import setup, find_packages
def post_install():
    # Get the user's home directory
    home_dir = os.path.expanduser('~')
    # Path to the bin directory where scripts are installed
    bin_dir = os.path.join(home_dir, '.local', 'bin')
    # Add the bin directory to the user's PATH
    rc_file = os.path.join(home_dir, '.bashrc') if os.path.exists(os.path.join(home_dir, '.bashrc')) else os.path.join(home_dir, '.zshrc')
    with open(rc_file, 'a') as f:
        f.write(f'\nexport PATH="$PATH:{bin_dir}"\n')


setup(
    name='auth-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'bjs-cli=auth.cli:cli',
        ],
    },
    cmdclass={"install": post_install}
)
