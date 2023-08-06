import setuptools

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
        name='pisten',
        version='0.1.1',
        author='David Pratt',
        author_email='davidpratt512@gmail.com',
        description='A simple magic packet forwarder',
        license='MIT',
        long_description=readme,
        long_description_content_type='text/markdown',
        keywords='wakeonlan wake-on-lan port-forwarding magic-packet',
        python_requires='>=3',
        url='https://github.com/davidpratt512/pisten',
        packages=setuptools.find_packages(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: System Administrators',
            'Topic :: System :: Networking',
            'Programming Language :: Python :: 3 :: Only',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent'
            ],
        entry_points={
            'console_scripts': ['pisten = pisten:main']
        }
)

