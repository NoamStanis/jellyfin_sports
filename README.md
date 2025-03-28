# *`NO LONGER MAINTAINED`*

# jellyfin_sports

### **For Educational Purposes Only**

## Description

Stream sports events straight from your Jellyfin server. jellyfin_sports allows users to scrape for live
streamed events and watch straight from Jellyfin. jellyfin_sports also generates meta-data that is used
in Jellyfin to provide a great viewing experience.

Currently, jellyfin_sports supports NBA, NHL, NFL and Premier League livestreams, but we plan to support other leagues in the future.


## Installation

### Pip

To install jellyfin_sports with pip, follow the steps bellow:


```bash
pip install jellyfin_sports --no-binary=jellyfin_sports
```


### Docker

To install jellyfin_sports with Docker, follow the steps bellow:

```bash
git clone https://github.com/axelmierczuk/jellyfin_sports.git
cd jellyfin_sports
docker build --tag jellyfin_sports .
docker run -v <Path Where You Want Output>:/jellyfin_sports/output jellyfin_sports 

# For example: docker run -v ~/Desktop:/jellyfin_sports/output jellyfin_sports 
# You can edit the paramaters that jellyfin_sports runs with from the Dockerfile
```

_OR_ you may pull the container with the following:

```bash
docker pull jellyfin_sports/jellyfin_sports:latest 
docker run -v <Path Where You Want Output>:/jellyfin_sports/output jellyfin_sports/jellyfin_sports:latest

# You CANNOT edit the paramaters that jellyfin_sports runs with when pulling the image
```

## Usage

We highly recommend running jellyfin_sports in combination with [tmux](https://man7.org/linux/man-pages/man1/tmux.1.html), or something similar.

Example usage:

```bash
python3 -m jellyfin_sports <arguments>
```

Start the jellyfin_sports server as follows:
```bash
# -nba specifies finding streams for the NBA
# -s allows jellyfin_sports to use Selenium to scrape
# -v enables verbose mode
# -o enables selecting output location

python3 -m jellyfin_sports -nba -s -v -o ~/Desktop
```

```bash
# -vv specifies silent mode (no output will be produced)
# -a specifies all leagues supported by jellyfin_sports

python3 -m jellyfin_sports -a -vv
```

**See the full list of arguments [here](https://jellyfin_sports-doc.readthedocs.io/en/latest/usage.html#installation).**

Once you have run the program, make sure to link to the .m3u's in the Jellyfin dashboard:

`Dashboard > Live TV > Tuner Devices (+) > Tuner Type (M3U Tuner) > File or URL (enter path)`

!['Dashboard'](https://i.ibb.co/7Vxvqkp/Screen-Shot-2022-01-11-at-10-47-26-AM.png)

!['Dashboard'](https://i.ibb.co/VH6b0Hc/Screen-Shot-2022-01-11-at-10-47-42-AM.png)

Additionally, make sure to change the "Refresh Guide" setting under:

`Dashboard > Scheduled Tasks > Live TV > Refresh Guide > Task Triggers`


!['Dashboard'](https://i.ibb.co/q7mhTMt/Screen-Shot-2022-01-11-at-10-58-57-AM.png)

!['Dashboard'](https://i.ibb.co/JxcdXC3/Screen-Shot-2022-01-11-at-10-59-11-AM.png)

Once the path has been defined and the settings have been updated, you can check out your streams under:

`Home > Live TV > Channels (at the top)`

!['Dashboard'](https://i.ibb.co/yS5ycS6/Screen-Shot-2022-01-11-at-11-08-08-AM.png)

## Documentation

Find all the documentation [here](https://jellyfin_sports-doc.readthedocs.io/en/latest/index.html).

## Future Improvement

Add server functionality, aka, ability to access streams (m3u files) from HTTP server.
