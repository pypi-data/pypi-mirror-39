from distutils.core import setup

setup(
    name='qrdecode',
    version='1.0.4',
    description='decode QRCode data',
    long_description='decode QRCode data',
    author='zhangyun',
    author_email='zhangyun@fenbi.com',
    keywords=['pip3', 'qrdecode', 'python3', 'python', 'qrcode'],
    url='http://pip.zhenguanyu.com/',
    packages=['qrdecode'],
    package_data={'qrdecode': ['*.py', '*.jpg']},
    license='MIT',
    install_requires=['ybc_config', 'requests', 'ybc_exception'],
)
