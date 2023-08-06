### dir2opus

dir2opus converts mp3, m4a, and wav files to the free open source Opus format. Opus files are
about 20-25% smaller than mp3s with the same relative sound quality. Your mileage may vary.

### Installation
Install with `sudo pip2 install dir2opus` and use with `dir2opus`.

Other options for installation:   
- Download this repo, install with `sudo sh install.sh` and use with `dir2opus`.
- If you do not have root access: Download the file `dir2opus`. Each time you use dir2opus, call it with e.g. `python2 ~/Downloads/dir2opus`.  

### Requirements
 - Tag preservation: mutagen (http://www.sacredchao.net/quodlibet/wiki/Development/Mutagen)
 - M4A Conversion: faad or mplayer (ALAC: alac-decoder)
 - WMA Conversion: mplayer
 - MP3 Conversion: mpg123, mpg321, lame or mplayer
 - FLAC Conversion: flac or ogg123
 - Ogg Vorbis Conversion: oggdec or ogg123
 - CD Ripping: cdparanoia, icedax or mplayer

### Usage
 Read the manpage for detailed instructions: "man dir2opus", or type "dir2opus
 --help" for brief usage details. The script is extremely simple, so you
 shouldn't have any troubles figuring it out.

 Dir2opus can take multiple filenames as arguments, and will Do The Right Thing
 based on the file extension. If using the '-d' flag, you may only give directories
 as arguments, not filenames and directories

 If you wish to convert m4a, wma and/or wav files using -d then the -m, -f and -w
 flags must be used respectively (FLAC: --convert-flac). Wav files are deleted
 by default, use -p to keep wav files after conversion.

 There is also support for CD ripping using the '-c' flag. This functionality
 is not well supported, and it may be better to use a different program for
 such a task.

### File overview
 COPYING    - The License under which dir2opus is released.
 NEWS       - Changes between the versions
 install.sh - A bash script to automate installation.
 dir2opus    - The script itself.
 dir2opus.1  - The manpage for dir2opus

### License and Disclaimer
 Copyright (c) 2007-2008 Julian Andres Klode
 Copyright (c) 2003-2006 Darren Kirby
 Copyright (c) 2013      Emery Hemingway

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

### Authors 
Current Developer:
- Emery Hemingway <emery@fuzzlabs.org>

Inactive Developers:
- Julian Andres Klode <jak@jak-linux.org>
- Darren Kirby <d@badcomputer.org>

Contributors:
- Cameron Stone <camerons@cse.unsw.edu.au>
- Marek Palatinus <marek@palatinus.cz>
