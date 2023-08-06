## pyMediaAnnotator

[![pipeline status](https://aalok-sathe.gitlab.io/pyMediaAnnotator/build.svg?v=8822633746006851841)](https://gitlab.com/aalok-sathe/pyMediaAnnotator/)

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

#### From pyPI using `pip`:
    python3 -m pip install --upgrade [--user] pyMediaAnnotator

The `--user` flag installs it locally
without needing `root` (optional).

If you are able to ensure the availability
of GTK bindings from some other source,
you could skip installing pyGTK:

    python3 -m pip install --upgrade [--user] --no-deps pyMediaAnnotator

#### From source
- Clone the repository
    - `git clone https://gitlab.com/aalok-sathe/pyMediaAnnotator.git`
- Make sure to have the necessary prerequisites:
    - `pyGTK/pyGTK/pyGObject`: Python GTK bindings
    - `vlc`, `python-vlc`: the VLC media player and Python bindings for `libvlc`
- Create Python package and install:
    - `make build`
    - `python3 setup.py install`

### Usage:
- Start application with the executable: `./pyMediaAnnotator`
- Screenshot (v0.1.2): example usage to annotate the laugh track in an episode of Friends ![example usage](scrsht-friends.png?raw=true Screenshot")

### Compatibility:
- GNU/Linux, \*NIX [recommended]:
    - Expected to run with proper prerequisites
    - Tested on Ubuntu 16.04
- Any other system:
    - Not tested, however, should theoretically work long as you are able to provide pyGTK and libvlc support
