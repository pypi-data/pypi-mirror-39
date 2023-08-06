#!/usr/bin/python2

from setuptools import setup

setup(name='dir2opus',
      version='0.12.0',
      description='converts folders with audio files to the more space efficient Opus format',
      long_description='''dir2opus converts mp3, m4a, and wav files to the free open source Opus format. Opus files are
about 20-25% smaller than mp3s with the same relative sound quality. Your mileage may vary.

Keep in mind that converting from mp3 or m4a to opus is a conversion between two lossy formats.
This is fine if you just want to free up some disk space, but if you're a hard-core audiophile
you may be dissapointed. I really can't notice a difference in quality with 'naked' ears myself.

This script converts mp3s to wavs using mpg123 then converts the wavs to opus using opusenc.
m4a conversions require faad. Id3 tag support requires mutagen for mp3s.
Scratch tags using the filename will be written for wav files (and mp3s with no tags!)''',
      url='https://github.com/ehmry/dir2opus',
      license='GPL3',
      scripts=['dir2opus']
      )
