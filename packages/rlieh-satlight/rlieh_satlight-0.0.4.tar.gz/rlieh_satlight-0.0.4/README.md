# RLIEH Sat light

This module is intended to provide a python3 module and a CLI tool to manage
light phases on a RLIEH sat system

Rlieh-satlight is a part of the [RLIEH project](http://www.emnet.cc/portfolio/rlieh/)
and can be used on any system running python.

## .ini file sample
```ini
[hardware]
type = sat
ip = 192.168.1.43
pwm_channel = 0
; type = controller
; pin = 18

; light pwm values (percent)
[light_thresholds]
dawn = [0, 20]
sunrise = [20, 75]
noon = [75, 100, 75] ; unused
sunset = [75, 20]
dusk  = [20, 0]

; light modulation phases duration (in mn)
[light_duration]
dawn = 10
sunrise = 10
sunset = 10
dusk = 10
```


## Install

### From source

```bash
git clone https://work.ipeos.com/gitlab/rlieh/rlieh-sat-light-client.git
cd rlieh-satlight
python3 setup.py install
```
coming soon to https://github.com/owatte/rlieh-satlight.git

### From pip

coming soon
```
pip3 install rlieh-satlight
```
## Usage

### as Py module
```python
  >>> from rlieh_sat.core import RliehSatLight
  >>> light = RliehSatLight('/home/pi/conf/matouba.ini', 'dawn')
  >>> light.request()
```

### as CLI tool

```bash
$ rlieh-satlight -h
usage: rlieh-satlight [-h] -i INI -p PHASE

Manage light on RLIEH sat.

optional arguments:
  -h, --help               show this help message and exit
  -i INI, --ini INI        ini file full path
  -p PHASE, --phase PHASE  light phase

```

#### Simple call example
*dawn* phase on *matouba* tank

 ```
$ rlieh-satlight -i /home/pi/conf/matouba.ini -p dawn
```

#### Tip : create an alias

If you manage several tanks, the best way is probably to create aliases

```bash
$ alias matouba_dawn='rlieh-satlight -i /home/pi/conf/matouba.ini -p dawn'
```
## Licence

Released under The [GPL v3 License](COPYING.md).

Copyright (C) 2018 EmNet
