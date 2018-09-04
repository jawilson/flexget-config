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
1. My custom ``content_sort`` plugin ([available in this repository](https://github.com/jawilson/flexget-config/blob/master/flexget/plugins/content_sort.py)) changes the ``move_done`` value if the torrent contains a ``.rar``
1. The torrent is added to Deluge
1. Deluge is configured with the [Execute](http://dev.deluge-torrent.org/wiki/Plugins/Execute) plugin to run my ``trigger-decompress.sh`` script ([also available in this repository](https://github.com/jawilson/dotfiles/blob/master/deluge/trigger-decompress.sh)) when any torrent is done downloading
1. ``trigger-decompress.sh`` simply calls the Flexget API and requests the ``Series-Decompress`` and ``Movies-Decompress`` tasks be run
1. Flexget uses the ``decompress`` plugin to unpack the torrent to a 'staging' location, then it runs the appropriate ``*-Sort-Decompressed`` task
1. The sort task checks for files in the 'staging' location from step #6 and renames and moves the files to their appropriate final location
