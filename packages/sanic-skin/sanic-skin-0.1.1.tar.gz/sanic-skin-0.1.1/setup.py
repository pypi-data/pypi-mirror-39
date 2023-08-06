from setuptools import setup


setup(
    name='sanic-skin',
    version='0.1.1',
    packages=['sanic_skin'],
    url='https://github.com/beforeicer/sanic_skin',
    license='MIT License',
    author='hoo',
    author_email='beforeicer@126.com',
    keywords="sanic like tornado style",
    install_requires=['sanic>=0.8.3', 'asyncpg>=0.18.2', 'aioredis>=1.2.0'],
    description='a wrapper for sanic in order to code in a tornado-like way',
    long_description='a wrapper for sanic in order to code in a tornado-like way',
    platforms="any",
)

