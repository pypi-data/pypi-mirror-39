from setuptools import setup, find_packages


setup(name='rf_kv_client',
      version='0.0.6',
      description='RedForester bindings for Astorage KV',
      classifiers=[
                'Development Status :: 3 - Alpha',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.6',
            ],
      url='https://redforester.com',
      author='Red Forester',
      author_email='tech@redforester.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'python-dateutil==2.6.1',
            'urllib3==1.24.1',
            'acapelladb==0.3.5'
      ],
      include_package_data=True,
      zip_safe=False
)
