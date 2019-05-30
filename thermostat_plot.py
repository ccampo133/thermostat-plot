from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Input variables
START_DATE = '2019-05-01'
END_DATE = '2019-05-23'
DATA_DIR = 'data'
DATA_FILENAME = 'CampoHome_20190530124626.csv'
SHOULD_PLOT_ON_OFF_MARKERS = False
INTERACTIVE_MODE = False

# Constants
DATA_FILE_PATH = DATA_DIR + '/' + DATA_FILENAME
DATETIME_FORMAT = '%m/%d/%Y%I:%M %p'
COOL_SETPOINT = 'Cool setpoint set to '
NEW_TEMP = 'New temperature '
HUMIDITY = 'Humidity '
COOLING_START = 'Set to Cooling'
IDLE_START = 'Set to System Idle'
COLUMNS = {
    'date': 0,
    'time': 1,
    'user': 2,
    'device': 3,
    'event': 4
}


def pad_with_previous_val(*argv):
    for val in argv:
        if len(val) != 0:
            val.append(val[-1])
        else:
            val.append(None)


def pad_with_none(*argv):
    for val in argv:
        val.append(None)


def main():
    if INTERACTIVE_MODE:
        plt.ion()

    # Columns: date, time, user, device, event
    data = pd.read_csv(DATA_FILE_PATH, quotechar='"', skipinitialspace=True).values

    # Collect only the relevant data we care about
    datetimes = []
    set_temps = []
    actual_temps = []
    humidity = []
    cooling_starts = []
    for row in data:
        event = row[COLUMNS['event']]

        if event.startswith(NEW_TEMP):
            actual_temp = int(event[len(NEW_TEMP):])
            actual_temps.append(actual_temp)
            pad_with_previous_val(set_temps)
            pad_with_none(cooling_starts, humidity)
        elif event.startswith(COOL_SETPOINT):
            set_temp = int(event[len(COOL_SETPOINT):])
            set_temps.append(set_temp)
            pad_with_none(cooling_starts, actual_temps, humidity)
        elif event.startswith(HUMIDITY):
            cur_humidity = int(event[len(HUMIDITY):-1])  # Remove the % symbol
            humidity.append(cur_humidity)
            pad_with_previous_val(set_temps)
            pad_with_none(cooling_starts, actual_temps)
        elif event.startswith(COOLING_START):
            cooling_starts.append(True)
            pad_with_previous_val(set_temps)
            pad_with_none(actual_temps, humidity)
        elif event.startswith(IDLE_START):
            cooling_starts.append(False)
            pad_with_previous_val(set_temps)
            pad_with_none(actual_temps, humidity)
        else:
            continue

        date = row[COLUMNS['date']]
        time = row[COLUMNS['time']]
        dt = datetime.strptime(date + time, DATETIME_FORMAT)
        datetimes.append(dt)

    # Convert to arrays, for plotting and other manipulation
    datetimes = np.array(datetimes)
    set_temps = np.array(set_temps)
    actual_temps = np.array(actual_temps)
    humidity = np.array(humidity)
    cooling_starts = np.array(cooling_starts)

    # Trim to date range
    if START_DATE is not None and END_DATE is not None:
        start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
        end_date = datetime.strptime(END_DATE, '%Y-%m-%d')
        i1 = np.where(datetimes >= start_date)
        i2 = np.where(datetimes <= end_date)
        indices = np.intersect1d(i1, i2)
    elif START_DATE is not None:
        start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
        indices = np.where(datetimes >= start_date)
    elif END_DATE is not None:
        end_date = datetime.strptime(END_DATE, '%Y-%m-%d')
        indices = np.where(datetimes <= end_date)
    else:
        indices = None

    datetimes = datetimes[indices]
    set_temps = set_temps[indices]
    actual_temps = actual_temps[indices]
    humidity = humidity[indices]
    cooling_starts = cooling_starts[indices]

    # Plot
    plt.clf()
    # noinspection PyTypeChecker
    fig, axes = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [4, 1]})
    axes[0].set_ylabel('Temperature (F)')
    axes[0].plot(datetimes[np.where(actual_temps)], actual_temps[np.where(actual_temps)], color='blue',
                 label='Recorded Temperature')
    axes[0].plot(datetimes, set_temps, color='red', label='Set Temperature')
    axes[0].legend()
    axes[0].grid(b=True, which='major', linestyle='-', alpha=0.5)

    axes[1].set_xlabel('Date and Time (EDT)')
    axes[1].set_ylabel('Humidity (%)')
    axes[1].plot(datetimes[np.where(humidity)], humidity[np.where(humidity)])
    axes[1].grid(b=True, which='major', linestyle='-', alpha=0.5)

    # Set tick font size
    for ax in axes:
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(8)

    # Plot on/off markers
    if SHOULD_PLOT_ON_OFF_MARKERS:
        for i in range(len(cooling_starts)):
            if cooling_starts[i] is True:
                axes[0].axvline(datetimes[i], color='cyan', alpha=0.2)
            elif cooling_starts[i] is False:
                axes[0].axvline(datetimes[i], color='red', alpha=0.2)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
