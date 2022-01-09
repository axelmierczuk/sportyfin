# Sportyfin

## Description

Stream sports events straight from your Jellyfin server. Sportyfin allows users to scrape for live
streamed events and watch straight from Jellyfin. Sportyfin also generates meta-data that is used
in Jellyfin to provide a great viewing experience.

Currently, Sportyfin supports NBA, NHL and NFL livestreams, but we plan to support other leagues in the future.


## Installation

To install Sportyfin with your running instance of Jellyfin, follow the steps bellow:


```bash
pip install sportyfin --no-binary=sportypy
```

To uninstall the program:

```bash
pip uninstall sportyfin
```


## Usage

We highly recommend running Sportyfin in combination with [tmux](https://man7.org/linux/man-pages/man1/tmux.1.html), or something similar.

Example usage:

```bash
python3 -m sportyfin #arguments
```

Start the sportyfin server as follows:
```bash
# -nba specifies finding streams for the NBA
# -s allows sportyfin to use Selenium to scrape
# -v enables verbose mode

python3 -m sportyfin -nba -s -v
```

```bash
# -vv specifies silent mode (no output will be produced)
# -a specifies all leagues supported by sportyfin
python3 -m sportyfin -a -vv
```

## Documentation

Find all the documentation [here]() (will update link with documentation once it is finished).