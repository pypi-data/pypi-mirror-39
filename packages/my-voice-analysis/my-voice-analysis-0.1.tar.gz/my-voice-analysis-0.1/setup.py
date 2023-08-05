from setuptools import setup

setup(name='my-voice-analysis',
      version='0.1',
      description='the analysis of voice (simultaneous speech) without the need of a transcription',
      url='https://github.com/Shahabks/my-voice-analysis',
      author='Shahab Sabahi',
      author_email='sabahi.s@mysol-gc.jp',
      license='MIT',
      classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.7',
		],
	  keywords='praat speech signal processing phonetics',
	  install_requires=[
		'numpy>=1.15.2',
		'praat-parselmouth>=0.3.2',
		'pandas>=0.23.4',
		'scipy>=1.1.0',
		],
	  packages=['my-voice-analysis'],
      zip_safe=False)
	  
