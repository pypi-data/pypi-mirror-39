from distutils.core import setup

setup(
    name='ybc_camera',
    packages=['ybc_camera'],
    version='1.0.4',
    description='ybc camera',
    long_description='ybc camera',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'python3', 'python', 'camera'],
    license='MIT',
    package_data={'ybc_camera': ['*.py']},
    install_requires=['opencv-python', 'ybc_exception']
)
