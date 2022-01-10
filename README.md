# Sportyfin

## Description

Stream sports events straight from your Jellyfin server. Sportyfin allows users to scrape for live
streamed events and watch straight from Jellyfin. Sportyfin also generates meta-data that is used
in Jellyfin to provide a great viewing experience.

Currently, Sportyfin supports NBA, NHL, NFL and Premier League livestreams, but we plan to support other leagues in the future.


## Installation

To install Sportyfin with your running instance of Jellyfin, follow the steps bellow:


```bash
pip install sportyfin --no-binary=sportyfin
```

To uninstall the program:

```bash
pip uninstall sportyfin
```


## Usage

We highly recommend running Sportyfin in combination with [tmux](https://man7.org/linux/man-pages/man1/tmux.1.html), or something similar.

Example usage:

```bash
python3 -m sportyfin -url "SomeURL" #arguments
```

Start the sportyfin server as follows:
```bash
# -nba specifies finding streams for the NBA
# -s allows sportyfin to use Selenium to scrape
# -v enables verbose mode
# -o enables selecting output location

python3 -m sportyfin -nba -s -v -o ~/Desktop -url "SomeURL"
```

```bash
# -vv specifies silent mode (no output will be produced)
# -a specifies all leagues supported by sportyfin

python3 -m sportyfin -a -vv -url "SomeURL"
```

Once you have run the program, make sure to link to the .m3u's in the Jellyfin dashboard:

`Dashboard > Live TV > Tuner Devices (+) > Tuner Type (M3U Tuner) > File or URL (enter path)`

Once the path has been defined, you can check out your streams under:

`Home > Live TV > Channels (at the top)`

## Documentation

Find all the documentation [here](https://sportyfin-doc.readthedocs.io/en/latest/index.html).


## Update

As of 0.1.13, you now **need** to provide your own url to scrape since this is not a tool that should be used for piracy. Try: https://sportscentral.io for example.


## Future Improvement

Add server functionality, aka, ability to access streams (m3u files) from HTTP server.
