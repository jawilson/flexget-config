# [Flexget](http://www.flexget.com) Configuration Files

Created by: [Jeff Wilson](mailto:jeff@jeffalwilson.com)  
Available from: https://github.com/jawilson/flexget-config (originally located in https://github.com/jawilson/dotfiles)

I'm using the [secrets](http://flexget.com/wiki/Plugins/secrets) plugin to hide my private credentials for various plugins. If you want to do this as well, you will need to create a ``secretfile.yml`` file in the same directory as your ``config.yml``.

## Installation
1. Install [Flexget](http://www.flexget.com)
1. Clone this repository into the `.flexget` directory of your home directory
    ```bash
    git clone https://github.com/jawilson/flexget-config.git .flexget
    ```
1. Set up your `secretfile.yml`
1. Run the Flexget daemon
    ```bash
    flexget daemon start -d
    ```

I've also added the following line to my local crontab (`crontab -e`):
```
@reboot /usr/local/bin/flexget daemon start -d >/dev/null 2>&1
```

## Rar-unpacking

My entire setup results in a single video file (``.mkv``, ``.mp4``, etc) in the final destination with a nice name regardless if it's packed in a rar or not.
Here's the gist of how it works:
1. Flexget accepts the torrent regardless if it's a rar-pack or not
1. My custom ``content_sort`` plugin ([available in this repository](https://github.com/jawilson/flexget-config/blob/master/plugins/content_sort.py)) changes the ``move_done`` value if the torrent contains a ``.rar``
1. The torrent is added to Deluge
1. Deluge is configured with the [Execute](http://dev.deluge-torrent.org/wiki/Plugins/Execute) plugin to run my ``deluge_torrent_complete`` script ([also available in this repository](https://github.com/jawilson/dotfiles/blob/master/bin/deluge_torrent_complete)) when any torrent is done downloading
1. ``deluge_torrent_complete`` checks if the torrent is located in the directory we set in step #2, if not it skips to the last step
1. ``deluge_torrent_complete`` unpacks the first .rar file it finds in the torrent to a 'staging' location
1. ``deluge_torrent_complete`` calls flexget with a completely separate config, ``sorting.yml`` ([also available in this repository](https://github.com/jawilson/flexget-config/blob/master/sorting.yml))
1. The ``sorting.yml`` config checks for files in the 'staging' location from step #6 and renames and moves the files to their appropriate final location

## To Do
1. Replace rar-unpacking script with Flexget task ([#1](https://github.com/jawilson/flexget-config/issues/1))
