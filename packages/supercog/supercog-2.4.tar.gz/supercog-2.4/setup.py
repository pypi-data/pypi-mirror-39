from distutils.core import setup
  
setup(
    name = 'supercog',
    packages = ['supercog'],
    version = '2.4',
    license='MIT',
    description = 'A project that assists in making a Discord bot. Includes HTML and Markdown support.',
    author = 'FellowHashbrown',
    author_email = 'fellowhashbrown@gmail.com',
    url = 'https://github.com/FellowHashbrown/supercog',
    download_url = 'https://github.com/FellowHashbrown/supercog/archive/v2.4.tar.gz',
    keywords = ["discord", "bot", "cogs", "extensions", "command", "category", "html", "markdown"],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)