from nose import tools as nt
from ndtest import model

import math


class TestBox(object):

    def test_aw_constraints(self):
        with nt.assert_raises(ValueError) as context:
            model.Box(100, 20, 361, 1)
        nt.assert_equal('Box accepts both a and w <= 360; got a=361, w=1', context.exception.message)
        with nt.assert_raises(ValueError) as context:
            model.Box(100, 20, 1, 361)
        nt.assert_equal('Box accepts both a and w <= 360; got a=1, w=361', context.exception.message)

    def test_area(self):
        pb = model.Box(100, 21.3, 100, 21.3)
        area = pb.area()
        nt.assert_almost_equal(21.3 * math.radians(21.3), area)

    def test__eq__equal(self):
        pb1 = model.Box(120, 40, 20, 60)
        pb2 = model.Box(120, 40, 20, 60)
        nt.assert_equal(pb1, pb2)

    def test__eq__different_along_x(self):
        pb1 = model.Box(120, 40, 20, 60)
        pb2 = model.Box(121, 40, 20, 60)
        nt.assert_not_equal(pb1, pb2)
        pb1 = model.Box(120, 40, 20, 60)
        pb2 = model.Box(120, 41, 20, 60)
        nt.assert_not_equal(pb1, pb2)

    def test__eq__different_along_a(self):
        pb1 = model.Box(120, 40, 20, 60)
        pb2 = model.Box(120, 40, 21, 60)
        nt.assert_not_equal(pb1, pb2)
        pb1 = model.Box(120, 40, 20, 60)
        pb2 = model.Box(120, 40, 20, 61)
        nt.assert_not_equal(pb1, pb2)


class TestBoundBox(object):

    def test_aw_constraints(self):
        with nt.assert_raises(ValueError) as context:
            model.BoundBox(100, 20, 360, 1)
        nt.assert_equal('BoundBox accepts a + w <= 360, got 361', context.exception.message)

    def test__repr__equal(self):
        pb = model.BoundBox(120, 40, 20, 60)
        nt.assert_equal('<BoundBox [x=120,l=40,a=20,w=60]>', repr(pb))

    def test_overlap_empty_x_aligned(self):
        pb1 = model.BoundBox(120, 40, 20, 60)
        pb2 = model.BoundBox(160, 40, 20, 60)
        nt.assert_is_none(pb1.overlap(pb2))
        nt.assert_is_none(pb2.overlap(pb1))

    def test_overlap_empty_a_aligned(self):
        pb1 = model.BoundBox(120, 40, 20, 40)
        pb2 = model.BoundBox(120, 40, 60, 100)
        nt.assert_is_none(pb1.overlap(pb2))
        nt.assert_is_none(pb2.overlap(pb1))

    def test_overlap_equals(self):
        pb1 = model.BoundBox(120, 40, 20, 40)
        pb2 = model.BoundBox(120, 40, 20, 40)
        nt.assert_equal(pb1, pb2)
        pb12 = pb1.overlap(pb2)
        pb21 = pb2.overlap(pb1)
        nt.assert_equal(pb12, pb21)
        nt.assert_equal(pb1, pb12)

    def test_overlap_x_aligned(self):
        pb1 = model.BoundBox(120, 40, 20, 40)
        pb2 = model.BoundBox(159, 50, 20, 40)
        exp = model.BoundBox(159, 1, 20, 40)
        nt.assert_equal(exp, pb1.overlap(pb2))
        nt.assert_equal(exp, pb2.overlap(pb1))

    def test_overlap_a_aligned(self):
        pb1 = model.BoundBox(120, 40, 20, 40)
        pb2 = model.BoundBox(120, 40, 59, 40)
        exp = model.BoundBox(120, 40, 59, 1)
        nt.assert_equal(exp, pb1.overlap(pb2))
        nt.assert_equal(exp, pb2.overlap(pb1))


class TestPipeBox(object):

    def test__repr__equal(self):
        pb = model.PipeBox(1, 20, 100, 30, 260)
        nt.assert_equal('<PipeBox [id=1,x=20,l=100,a=30,w=260]>', repr(pb))

    def test_plain_regions_one(self):
        pb = model.PipeBox(1, 20, 100, 30, 260)
        regions = pb.plain_regions
        nt.assert_equal(1, len(regions))
        nt.assert_equal(regions[0], model.BoundBox(20, 100, 30, 260))

    def test_plain_regions_two(self):
        pb = model.PipeBox(1, 20, 100, 200, 200)
        regions = pb.plain_regions
        nt.assert_equal(2, len(regions))
        nt.assert_equal(regions[0], model.BoundBox(20, 100, 0, 200 + 200 - 360))
        nt.assert_equal(regions[1], model.BoundBox(20, 100, 200, 160))

    def test_overlap_empty(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 70, 70)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(0, len(overlaps))
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_one_region_up(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 120, 180)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(1, len(overlaps))
        nt.assert_equal(model.BoundBox(20, 100, 200, 100), overlaps[0])
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_one_region_up_full(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 220, 130)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(1, len(overlaps))
        nt.assert_equal(model.BoundBox(20, 100, 220, 130), overlaps[0])
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_one_region_down(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 10, 180)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(1, len(overlaps))
        nt.assert_equal(model.BoundBox(20, 100, 10, 30), overlaps[0])
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_one_region_down_full(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 10, 30)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(1, len(overlaps))
        nt.assert_equal(model.BoundBox(20, 100, 10, 30), overlaps[0])
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_two_regions_external(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 220, 160)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(2, len(overlaps))
        expected_overlaps = [model.BoundBox(20, 100, 0, 20), model.BoundBox(20, 100, 220, 140)]
        nt.assert_equal(expected_overlaps, overlaps)
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_two_regions_internal(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 30, 180)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(2, len(overlaps))
        expected_overlaps = [model.BoundBox(20, 100, 30, 10), model.BoundBox(20, 100, 200, 10)]
        nt.assert_equal(expected_overlaps, overlaps)
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_three_regions_down(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 30, 340)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(3, len(overlaps))
        expected_overlaps = [model.BoundBox(20, 100, 0, 10), model.BoundBox(20, 100, 30, 10),
                             model.BoundBox(20, 100, 200, 160)]
        nt.assert_equal(expected_overlaps, overlaps)
        nt.assert_equal(overlaps, pb2.overlap(pb1))

    def test_overlap_three_regions_up(self):
        pb1 = model.PipeBox(1, 20, 100, 200, 200)
        pb2 = model.PipeBox(1, 20, 100, 270, 340)
        overlaps = pb1.overlap(pb2)
        nt.assert_equal(3, len(overlaps))
        expected_overlaps = [model.BoundBox(20, 100, 0, 40), model.BoundBox(20, 100, 200, 50),
                             model.BoundBox(20, 100, 270, 90)]
        nt.assert_equal(expected_overlaps, overlaps)
        nt.assert_equal(overlaps, pb2.overlap(pb1))
