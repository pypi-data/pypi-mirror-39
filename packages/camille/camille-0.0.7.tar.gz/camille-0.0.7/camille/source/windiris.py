import sqlite3
import os
import pandas as pd
from math import radians
import re

def _to_string(x):
    x = re.sub('[^A-Za-z0-9,.]', '', str(x))
    return '(' + x + ')'


def _sqlite(start_date,
            end_date,
            connection,
            installation,
            los_id=None,
            distance=None,
            status=None):
    connection.set_trace_callback(print)
    query = (
        'SELECT * FROM ' + installation #nosec
        + ' WHERE Timestamp >= :start AND Timestamp < :end'
        + ( '' if los_id is None
               else ' AND "LOS Index" IN {}'.format(_to_string(los_id)) )
        + ( '' if distance is None
               else ' AND Distance IN {}'.format(_to_string(distance)) )
        + ( '' if status is None
               else ' AND "RWS Status" IN {}'.format(_to_string(status)) )
        + ';'
    )

    df = pd.read_sql_query(query, connection,
                           params={
                                'start': str(start_date.replace(tzinfo=None)),
                                'end': str(end_date.replace(tzinfo=None))
                           },
                           index_col='Timestamp',
                           parse_dates={
                                'Timestamp': {'utc': True}
                           }).sort_index()

    df.rename(columns={
        'LOS Index': 'los_id',
        'Distance': 'distance',
        'RWS': 'radial_windspeed',
        'RWS Status': 'status',
        'Tilt': 'pitch',
        'Roll': 'roll',
    }, inplace=True)
    df.index.name = 'time'
    df.pitch = df.pitch.apply(radians)
    df.roll = df.roll.apply(radians)

    return df


def windiris(root):
    def windiris_internal(installation,
                          start_date,
                          end_date,
                          los_id=None,
                          distance=None,
                          status=None):
        f = os.path.join(root, installation, installation + '_rtd.db' )
        conn = sqlite3.connect(f)

        return _sqlite(start_date,
                       end_date,
                       conn,
                       installation,
                       los_id=los_id,
                       distance=distance,
                       status=status)

    return windiris_internal
