from nose import tools as nt
import mock
import cStringIO

from ndtest import loader
from ndtest import model


class TestLoader(object):

    CSV_PATH_MOCK = '/path/to/inspection_data.csv'
    CSV_HEADER = ('id', 'x', 'l', 'a', 'w')

    def _csv_text(self, rows, header=None):
        text_rows = ['\t'.join(self.CSV_HEADER if header is None else header)]
        for row in rows:
            text_rows.append('\t'.join((str(_) for _ in row)))
        return '\n'.join(text_rows)

    def test_load(self):
        with mock.patch('ndtest.loader.open') as open_mock:
            rows = [[1, 10, 20, 50, 20.0],
                    [2, 10, 20, 55, 20],
                    [3, 20, 20, 70, 10],  # This row must be put after the next by `loader.load` because of `a`
                    [4, 20, 20, 20, 20]]
            open_mock.return_value = cStringIO.StringIO(self._csv_text(rows))
            boxes = loader.load(self.CSV_PATH_MOCK)

            open_mock.assert_called_once()
            nt.assert_equal(mock.call(self.CSV_PATH_MOCK), open_mock.call_args)
            nt.assert_equal(len(boxes), 4)

            box = model.PipeBox(*rows[0])
            nt.assert_true(boxes[0].box_id, box.box_id)
            nt.assert_true(boxes[0], box)

            box = model.PipeBox(*rows[1])
            nt.assert_true(boxes[1].box_id, box.box_id)
            nt.assert_true(boxes[1], box)

            box = model.PipeBox(*rows[3])
            nt.assert_true(boxes[3].box_id, box.box_id)
            nt.assert_true(boxes[3], box)

            box = model.PipeBox(*rows[2])
            nt.assert_true(boxes[2].box_id, box.box_id)
            nt.assert_true(boxes[2], box)

    def test_load_invalid_header(self):
        with mock.patch('ndtest.loader.open') as open_mock:
            csv_text = self._csv_text([[1, 10, 20, 50, 20.0]], header=('id', 'x', 'l', 'column'))
            open_mock.return_value = cStringIO.StringIO(csv_text)
            with nt.assert_raises_regexp(loader.DataLoaderException, 'Invalid header. Expected '):
                loader.load(self.CSV_PATH_MOCK)
            open_mock.assert_called_once()
            nt.assert_equal(mock.call(self.CSV_PATH_MOCK), open_mock.call_args)

    def test_load_invalid_row(self):
        with mock.patch('ndtest.loader.open') as open_mock:
            csv_text = self._csv_text([[1, 10, 'XXX', 50, 20.0]])
            open_mock.return_value = cStringIO.StringIO(csv_text)
            with nt.assert_raises_regexp(loader.DataLoaderException, 'Invalid data at row 1. Columns must be numbers'):
                loader.load(self.CSV_PATH_MOCK)
            open_mock.assert_called_once()
            nt.assert_equal(mock.call(self.CSV_PATH_MOCK), open_mock.call_args)
