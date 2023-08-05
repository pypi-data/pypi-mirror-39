from setuptools import setup

setup(
    name = 'python3-anticaptcha',
    version = '1.0',
    author = 'AndreiDrang, redV0ID',

    packages = ['python3_anticaptcha'],
    install_requires = [
                        'requests==2.20.1',
                        'aiohttp==3.4.4',
                        'pika==0.12.0'
    ],
    description = 'Python 3 AntiCaptcha library with AIO module.',
    url = 'https://github.com/AndreiDrang/python3-anticaptcha',
    author_email = 'drang.andray@gmail.com',
    license = 'MIT',
    keywords = '''captcha 
                  anticaptcha 
				  python3
				  recaptcha
				  captcha
				  security
				  api
				  python-library
				  python-anticaptcha
				  anticaptcha-client''',
    python_requires = '>=3.6',
)
