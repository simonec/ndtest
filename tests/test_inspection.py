from nose import tools as nt

from ndtest import model
from ndtest import inspection


class TestOverlapMetadata(object):

    def test__repr__(self):
        metadata = inspection.OverlapMetadata(1, 2, [], 25, 33.2)
        nt.assert_equal("<OverlapMetadata [id_old=1,id_new=2,percent_old=25,percent_new=33.2]>", repr(metadata))


class TestInspectionsCollator(object):

    def test_analyze__old_after_new_along_a__empty(self):
        old_boxes = [model.PipeBox(1, 20, 20, 30, 20)]
        new_boxes = [model.PipeBox(1, 20, 20, 10, 20)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))

    def test_analyze__new_after_old_along_a__empty(self):
        old_boxes = [model.PipeBox(1, 20, 20, 10, 20)]
        new_boxes = [model.PipeBox(1, 20, 20, 30, 20)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))

    def test_analyze__old_after_new_along_x__empty(self):
        old_boxes = [model.PipeBox(1, 50, 40, 10, 20)]
        new_boxes = [model.PipeBox(1, 10, 40, 0, 20)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))

    def test_analyze__new_after_old_along_x__empty(self):
        old_boxes = [model.PipeBox(1, 10, 40, 0, 20)]
        new_boxes = [model.PipeBox(1, 50, 40, 10, 20)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))

    def test_analyze__old_circular_vs_new_plain__down(self):
        old_boxes = [model.PipeBox(1, 270, 100, 200, 320)]
        new_boxes = [model.PipeBox(1, 320, 100, 20, 40)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(1, len(data))
        nt.assert_in(1, data)
        nt.assert_equal(1, len(data[1]))
        nt.assert_in(1, data[1])

        metadata = data[1][1]
        nt.assert_equal(1, len(metadata.overlaps))
        nt.assert_equal(model.BoundBox(320, 50, 20, 40), metadata.overlaps[0])
        nt.assert_almost_equal(float(50 * 40) / float(100 * 40) * 100, metadata.percent_new)
        nt.assert_almost_equal(float(50 * 40) / float(100 * 320) * 100, metadata.percent_old)

    def test_analyze__new_circular_vs_old_plain__down(self):
        new_boxes = [model.PipeBox(1, 270, 100, 200, 320)]
        old_boxes = [model.PipeBox(1, 320, 100, 20, 40)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(1, len(data))
        nt.assert_in(1, data)
        nt.assert_equal(1, len(data[1]))
        nt.assert_in(1, data[1])

        metadata = data[1][1]
        nt.assert_equal(1, len(metadata.overlaps))
        nt.assert_equal(model.BoundBox(320, 50, 20, 40), metadata.overlaps[0])
        nt.assert_almost_equal(float(50 * 40) / float(100 * 320) * 100, metadata.percent_new)
        nt.assert_almost_equal(float(50 * 40) / float(100 * 40) * 100, metadata.percent_old)

    def test_analyze__old_circular_vs_new_plain__up(self):
        old_boxes = [model.PipeBox(1, 270, 100, 200, 320)]
        new_boxes = [model.PipeBox(1, 320, 100, 260, 40)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(1, len(data))
        nt.assert_in(1, data)
        nt.assert_equal(1, len(data[1]))
        nt.assert_in(1, data[1])

        metadata = data[1][1]
        nt.assert_equal(1, len(metadata.overlaps))
        nt.assert_equal(model.BoundBox(320, 50, 260, 40), metadata.overlaps[0])
        nt.assert_almost_equal(float(50 * 40) / float(100 * 40) * 100, metadata.percent_new)
        nt.assert_almost_equal(float(50 * 40) / float(100 * 320) * 100, metadata.percent_old)

    def test_analyze__new_circular_vs_old_plain__up(self):
        old_boxes = [model.PipeBox(1, 320, 100, 260, 40)]
        new_boxes = [model.PipeBox(1, 270, 100, 200, 320)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(1, len(data))
        nt.assert_in(1, data)
        nt.assert_equal(1, len(data[1]))
        nt.assert_in(1, data[1])

        metadata = data[1][1]
        nt.assert_equal(1, len(metadata.overlaps))
        nt.assert_equal(model.BoundBox(320, 50, 260, 40), metadata.overlaps[0])
        nt.assert_almost_equal(float(50 * 40) / float(100 * 320) * 100, metadata.percent_new)
        nt.assert_almost_equal(float(50 * 40) / float(100 * 40) * 100, metadata.percent_old)

    def test_analyze__old_circular_vs_new_plain__middle(self):
        old_boxes = [model.PipeBox(1, 270, 100, 200, 320)]
        new_boxes = [model.PipeBox(1, 320, 100, 160, 40)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))

    def test_analyze__new_circular_vs_old_plain__middle(self):
        old_boxes = [model.PipeBox(1, 320, 100, 160, 40)]
        new_boxes = [model.PipeBox(1, 270, 100, 200, 320)]

        data = inspection.Collator.analyze(old_boxes, new_boxes)

        nt.assert_equal(0, len(data))
