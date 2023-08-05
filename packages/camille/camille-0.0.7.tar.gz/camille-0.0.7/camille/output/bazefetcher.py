import os
import datetime
import pytz
import pandas as pd

def _to_midnight_utc(timestamp):
    """ Copied from bazefetcher, logic modified

    Converts a timestamp to an UTC timestamp, to midnight of the
    given date (00:00:00). All timestamps are converted to UTC if they
    have timezone information, and assumed to already be UTC if they
    have no timezone information.
    """
    try:
        timestamp = pytz.utc.localize(timestamp)
    except ValueError:
        timestamp = timestamp.astimezone(pytz.utc)
    timestamp = timestamp.replace(hour=0, minute=0, second=0)
    return timestamp


def _daterange(start_date, end_date):
    """
    Generates dates in range between start_date and end_date with one
    day difference starting from start_date.
    First calls _to_midnight_utc on both.
    :param start_date: Start date timestamp, inclusive.
    :param end_date: End date timestamp, exclusive. Note, that if end
    time date is later than midnight of that day, the midnight date
    will be generated. If the date is exactly at midninght,
    it's not generated
    :return:
    """
    if start_date != end_date:
        is_end_on_midnight = _to_midnight_utc(end_date) == end_date
        start_date = _to_midnight_utc(start_date)
        end_date = _to_midnight_utc(end_date)
        if is_end_on_midnight:
            end_date -= datetime.timedelta(days=1)
        while start_date <= end_date:
            next_day = start_date + datetime.timedelta(days=1)
            yield (start_date, next_day)
            start_date = next_day


def _generate_tag_location(
    root, tag_name, start_date, end_date, full_path=True, suffix=".json"
    ):
    """ Copied from bazefetcher, logic modified

    Generates and returns the path for storing a tag given a start and end
    date. With full_path=False it will return the relative path to the
    storage driver location
     """
    filename = "{}_{}_{}{}".format(
        tag_name,
        start_date.isoformat().replace(":", "."),
        end_date.isoformat().replace(":", "."),
        suffix)
    directory_name = tag_name
    path = os.path.join(directory_name, filename)
    if full_path:
        path = os.path.join(root, path)
    return path


def bazefetcher(root):
    if not os.path.isdir(root):
        raise ValueError('{} is not a directory'.format(root))

    def bazefetcher_internal(
            series, tag=None, start=None, end=None):
        """
        Stores the provided series of data under root folder specified
        during call of outer method.
        :param series: Indexed series of datetime information.
        Intended object: pandas.Series
        :param tag: Tag of the document, Must be specified
        :param start: Start datetime of the stored period (inclusive).
        If param is not provided, start element of series parameter is
        taken. Date should be timezone aware
        :param end: End datetime of the stored period (exclusive).
        If param is not provided, end element of series parameter is
        taken. Date should be timezone aware. Can't be earlier than
        start date param.
        :return: None
        """
        if tag is None:
            raise ValueError('tag must be specified')

        if start is None: start = series.index[0].to_pydatetime()
        if end is None: end = series.index[-1].to_pydatetime()

        if start.tzinfo is None or end.tzinfo is None:
            raise ValueError('dates must be timezone aware')

        if not start <= end:
            raise ValueError('start_date must be earlier than end_date')

        series = series[start:end]

        eps = datetime.timedelta(microseconds=1)

        for s, e in _daterange( start, end ):
            tag_path = _generate_tag_location( root,
                                              tag,
                                              s,
                                              e,
                                              full_path=True,
                                              suffix='.json.gz' )

            ts = series[s:e-eps]
            ts = pd.DataFrame( { 't':ts.index, 'v':ts.values } )

            if not os.path.exists(os.path.dirname(tag_path)):
                try:
                    os.makedirs(os.path.dirname(tag_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            ts.to_json(tag_path, compression='gzip', orient='records' )

    return bazefetcher_internal
