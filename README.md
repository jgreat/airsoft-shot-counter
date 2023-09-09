# airsoft-shot-counter


# Development Environment

## venv

### Activate the venv

```shell
source .venv/bin/activate
```

### Create the venv

```shell
python3 -m venv .venv
```

### Install python requirements.

```shell
pip3 install -r ./requirements.txt
```

## Install or update the Circuitpython libraries.

Use `circup` utility to add the imported libs to the device.  Must activate the venv so `circup` is in your path.

```shell
circup update --all
```


## Troubleshooting the CIRCUITPY

### Messed up FS

Stuck in RO mode.

```shell
# Find the device
df -h | grep CIRCUITPY
/dev/sda1              941K   17K  924K   2% /media/jgreat/CIRCUITPY

# unmount the filesystem
sudo umount /dev/sda1

# repair the filesystem
sudo dosfsck -w -r -l -a -v -t /dev/sdb1

# hit the reset button to remount
```
