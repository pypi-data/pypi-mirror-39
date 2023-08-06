## pyMediaAnnotator

[![pipeline status](https://aalok-sathe.gitlab.io/pyMediaAnnotator/build.svg?v=2018-12-19 02:00:34.612346)](https://gitlab.com/aalok-sathe/pyMediaAnnotator/pipeline)

#### A GTK+ and vlc based application for annotating video and audio files for classification tasks

### Features:
- Add text annotations time-locked to content in media file
- Annotate time accurate to the millisecond
- Jump to annotation start time to verify correctness
- Standard media playback features (play/pause, stop, seek)
- Change annotation task mid-video
- Edit annotation label for particular time segment
- Delete annotation entry
- Undo annotation segment (in the order of most recent)
- Sort annotations by starttime by clicking on column header so that you can go back and re-annotate a particular segment of media

### Planned features and bugfixes for future releases:
- The YAML format was chosen because it is convenient and human-readable. However, in the future, the user should be able to choose output format (`json`, `pickle`, `txt`, Numpy array, etc.)
- Fix seek bar synchronization with playback
- Multiple button support for rapid multiclass annotation
- Save and resume existing annotation

### Installation:
- Clone the repository (recommended: ssh)
    - ssh: `git clone git@gitlab.com:aalok-sathe/pyMediaAnnotator.git`
    - https: `git clone https://gitlab.com/aalok-sathe/pyMediaAnnotator.git`
- Make sure to have the necessary prerequisites:
    - `pyGTK/pyGTK/pyGObject`: Python GTK bindings
    - `vlc`, `python-vlc`: the VLC media player and Python bindings for `libvlc`
- Use makefile to create Python package and install:
    - `make build`
    - `python3 setup.py install [--user]`

### Usage:
- Start application with the executable: `./pyMediaAnnotator`
- Screenshot: ![example usage to annotate the presence of laugh track in an episode of Friends](scrsht-friends.png?raw=true Screenshot")

### Compatibility:
- GNU/Linux:
    - Expected to run with proper prerequisites
    - Debian/Ubuntu:
        - Tested on Ubuntu 16.04
- MacOS:
    - Not tested, however, expected to work with proper GTK support
- Windows:
    - Not tested, not expected to work; but you are welcome to try
