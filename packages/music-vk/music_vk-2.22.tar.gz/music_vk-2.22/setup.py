from setuptools import setup,find_packages
# __init__.py
__version__ = "2.22"
setup(name='music_vk',
      version='2.22',
      description='Приложение music_vk',
      long_description='Приложение music_vk',
      classifiers=[ 'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7', 'Topic :: Text Processing :: Linguistic',
                    ],
      keywords='music,vk,music_vk',
      url='https://music_vk.com/', author='ivan martemyanov',
      author_email='imartemy152@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'vk_api',
          'requests',
          'datetime',
          'requests',
          'Pillow',
          'tkinter',
          'clipboard'
          
      ],
      include_package_data=True,
      zip_safe=False
)
