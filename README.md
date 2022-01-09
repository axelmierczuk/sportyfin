# Sportyfin

## Description

Stream sports events straight from your jellyfin server. Sportyfin works by running a local HTTP server that serves 
m3u files capable of forking other streams. These forks allow you to have access to sports streams right from jellyfin.
Additionally, Sportyfin generates metadata on the livestreams for the best viewing experience.


Currently, Sportyfin supports NBA, NHL and NFL livestreams, but we plan to support other leagues in the future.


## Installation

To install Sportyfin with your running instance of Jellyfin, follow the steps bellow:

Clone the repo in your prefered way, for example:

```bash
git clone ""
```

Once you have cloned the repo, run the installation script:

```bash
cd sportyfin
sudo chmod +x install.sh
sudo ./install.sh
```

During the installation, you will be prompted to configure some settings:

```bash
# To be configured
```

Once the installation has finished, you should see streams start to populate on Jellyfin. To double-check that the
installation was successfully, you should be able to see the links to the .m3u in your Dashboard:

`Dashboard > Live TV > Tuner Devices`

To uninstall the program, simply run the `sportyfin uninstall`:

```bash
sportyfin uninstall
```


## Usage

We highly recommend running Sportyfin in combination with [tmux](https://man7.org/linux/man-pages/man1/tmux.1.html), or something similar.

After installing the package, you can run `sportyfin` to configure the server or run it. See bellow:

```bash
# Get helpful information on sportyfin
sportyfin -h
```

Start the sportyfin server as follows:
```bash
# --nba specifies finding streams for the NBA
# --s allows sportyfin to use Selenium to scrape
# --v enables verbose mode

sportyfin start --nba --s --v
```

```bash
# --vv specifies silent mode (no output will be produced)
# --a specifies all leagues supported by sportyfin
sportyfin start --a --vv
```

Stop the Sportyfin by issuing the following command:

```bash
sportyfin stop 
```