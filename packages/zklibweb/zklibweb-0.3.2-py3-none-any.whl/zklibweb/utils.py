from typing import List, Tuple
from datetime import datetime as dt
from .exceptions import ZklibWebParceException


def raw_data(data: str) -> List[Tuple[str, dt]]:
    """
    Return data to python format

    Arguments:
        data {str} -- Data in plain format

    Raises:
        ZklibWebParceException -- When the data isn't correct

    Returns:
        List[Tuple[str, dt]]
    """

    result = []
    for item in data.split('\n'):
        detail = item.split('\t')
        if len(detail) < 2:
            continue
        try:
            person_id = detail[0]
            date = dt.strptime(detail[2], '%Y-%m-%d %H:%M:%S')
            result.append([person_id, date])
        except IndexError:
            raise ZklibWebParceException()
    return result
