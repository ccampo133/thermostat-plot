# thermostat-plot

Plot some thermostat data.

Requires a directory called `data` with various CSV files.

Example CSV format:

    Date,Time,User,Device,Event
    03/29/2019,08:24 PM,Device Event,CampoStat,Humidity 50%
    03/29/2019,09:00 PM,Device Event,CampoStat,Cool setpoint set to 76
    ...

# Development

Set up a [virtualenv](https://docs.python.org/3/library/venv.html)

    python3 -m venv venv

Then activate it

    source venv/bin/activate

Then install

    pip install -r requirements.txt

It's helpful to install Jupyter as well

    python3 -m pip install --upgrade pip
    python3 -m pip install jupyter

When done, deactivate the virtualenv and enjoy your day

    deactivate
