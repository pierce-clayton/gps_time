# gps_time.py

gps_time gets your position from a serial gps sensor and determines your current timezone based on your location

## Usage

```bash
git clone https://github.com/technicholy/gps_time
cd gps_time
pip3 install -r ./requirements.txt
./gps_time.py
```

If your GPS sensor is not on /dev/ttyUSB0 or COM5, pass that in as an argument

```bash
./gps_time.py /dev/ttyACM0 # or python gps_time.py COM1
```