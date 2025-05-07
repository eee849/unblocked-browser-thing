# Unblocked Browser/OS Thing
A little thing i made for myself- praying i can host it

## Installation

It cannot watch videos on its own until you go to the xfce terminal and type "sudo tor" then go wherever you want on firefox and it will work perfectly, it is preconfigured with the proxy configuration.

Run 
```bash
docker build -t void-desktop .
```

```bash
docker run -it --rm \
  --shm-size=1g \
  -p 6080:6080 \
  --name void-desktop \
  void-desktop
```
once built, run that.

### Important info

After the run was successful, open port 6080 in your web browser from "Ports" in VScode or Codespaces. This should show you a list of files, or automatically go to the novnc client. If it does show a list of files, you want to click something like nvnc.html, not nvnc-lite.html.

THERE IS NO AUDIO YET!!!

IF RESIZING PROBLEMS OCCUR GO TO SETTINGS AND SELECT LOCAL SCALING INSTEAD OF REMOTE.

If you have issues please make a [issue](https://github.com/eee849/unblocked-browser-thing/issues)

### Prerequisites

Docker
```bash
sudo apt install docker
```
Use docker to build void-desktop

## Usage

Used as a unblocked OS/Browser for schools.



## Technologies

* Github Codespaces

## Acknowledgments And Info

For more info/documentation go to [here](https://eee849.github.io)

Nothing really inspired me to make this, just did for fun.

## License
An unblocked OS/Browser I made. [License](https://choosealicense.com/licenses/agpl-3.0/) agreements are here.
