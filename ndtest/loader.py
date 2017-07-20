import csv
import operator

import model


class DataLoaderException(Exception):
    """ Custom data loader exception """

CSV_HEADER = ['id', 'x', 'l', 'a', 'w']


def load(path):
    """ Load data from a csv file and return a list of boxes ordered by the position in the longitudinal axis
    and that in the circumferential one respectively.

    Parameters
    ----------
    path : str
        Path to csv file.

    Returns
    -------
    list[PipeBox]
    """
    reader = csv.reader(open(path), dialect=csv.excel_tab)
    first_row = reader.next()
    if first_row != CSV_HEADER:
        raise DataLoaderException('Invalid header. Expected %s got %s' % (CSV_HEADER, first_row))
    boxes = []
    for i, (box_id, x, l, a, w) in enumerate(reader):
        try:
            box_id = int(box_id)
            x, l, a, w = float(x), float(l), float(a), float(w)
        except ValueError:
            raise DataLoaderException('Invalid data at row %s. Columns must be numbers' % (i + 1))
        boxes.append(model.PipeBox(box_id, x, l, a, w))
    boxes.sort(key=operator.attrgetter('x', 'a'))
    return boxes


