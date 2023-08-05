# qoob
- foobar-like music player for Linux
- Written in Python 3 and Qt 5

# Main features
- Folder structure library organization
- Metadata is parsed from file header when available
- Missing metadata is guessed with regex, from title and folder structure
- Realtime library filter to quickly find a specific media
- Tray icon with playback control and notifications
- Customizable notification, title, and tooltip format
- Customizable sorting routine
- Hotkeys and command line interface
- Album art viewer
- Shuffle and repeat functions
- Human readable configuration, metadata and playlists

# Screenshots
**Player window**

![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/player_1.png)

![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/player_2.png)


**Customizable popup**

![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/popup.png)


**Preferences**

![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/preferences_general.png)


![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/preferences_appearance.png)


![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/preferences_viewer.png)


![alt tag](https://gitlab.com/william.belanger/qoob/raw/master/screenshots/preferences_popup.png)


# Command line interface
- Playback: --play --pause --play-pause --stop --previous --next --shuffle on/off --repeat off/all/single
- Delete current media from disk: --delete --delete-no-confirm
- Quiet flag (app not launched by cli): --quiet
- Load folder(s): --folder \<path 1\> \<path 2\>
- Load file(s): --file \<path 1\> \<path 2\>
- Exit application: --quit

# Hotkeys
- Space: play-pause
- Backspace: remove selection from playlist
- Delete: delete selection from disk
- Left arrow: skip 5 seconds backward
- Right arrow: skip 5 seconds forward
- Ctrl + X: cut selection
- Ctrl + C: copy selection
- Ctrl + V: paste selection

# Installation
- Arch based distros: install 'qoob-git' from the AUR
- Debian based distros (require python 3.6 or more):
    - sudo apt-get install python3-setuptools python3-pip
    - sudo pip3 install qoob
    - wget http://mirrors.kernel.org/ubuntu/pool/universe/q/qtmultimedia-opensource-src/libqt5multimediagsttools5_5.11.1-1ubuntu1_amd64.deb
    - sudo dpkg -i libqt5multimediagsttools5_5.11.1-1ubuntu1_amd64.deb

- Windows (untested):
    - Install the lastest version of Python, along with the PyPi utility (pip)
    - Open the command prompt (cmd.exe) with administrator privileges
    - Type 'python3 -m pip3 install pyqt5 mutagen'
    - Manually download the repository and extract it's content
    - Create a shortcut to run the script manually with 'python your_installation_path/qoob/\_\_init\_\_.py'
