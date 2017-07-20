import math


class Box(object):
    """ Represent a specific area in the pipeline. """

    def __init__(self, x, l, a, w):
        """
        Parameters
        ----------
        x : int/float
            Initial position (meters) in the longitudinal axis.
        l : int/float
            Length (meters) of the box.
        a : int/float
            Initial position (degrees) in the circumferential axis, with 0 <= a < 360.
        w : int/float
            Width (degrees) of the box, with 0 < w <= 360.
        """
        if a > 360 or w > 360:
            raise ValueError("Box accepts both a and w <= 360; got a={a}, w={w}".format(a=a, w=w))
        self.x = x
        self.l = l
        self.a = a
        self.w = w

    def __eq__(self, other):
        return self.x == other.x and self.l == other.l and self.a == other.a and self.w == other.w

    def __repr__(self):
        fields = 'x={x},l={l},a={a},w={w}'.format(x=self.x, l=self.l, a=self.a, w=self.w)
        return '<%s [%s]>' % (self.__class__.__name__, fields)

    def area(self):
        """ Area of the box normalized on the radius (i.e. area for one meter radius).

        Returns
        -------
        float
        """
        return math.radians(self.w) * self.l


class BoundBox(Box):
    """ BoundBox areas cannot be lay at the turn of a = 0 (or a = 360 degrees who is the same),
    meaning that we have the following constraint:
            a + w <= 360
    """

    def __init__(self, x, l, a, w):
        if a + w > 360:
            raise ValueError("BoundBox accepts a + w <= 360, got %s" % (a + w))
        super(BoundBox, self).__init__(x, l, a, w)

    def overlap(self, other):
        """ Returns a BoundBox representing the overlap area between `self` and `other`.
        It is a symmetrical method (i.e. self.overlap(other) == other.overlap(self))

        Parameters
        ----------
        other : BoundBox

        Returns
        -------
        BoundBox
            The overlap region.
        """
        if self.x + self.l <= other.x or other.x + other.l <= self.x:
            return None
        if self.a + self.w <= other.a or other.a + other.w <= self.a:
            return None
        x = max(self.x, other.x)
        l = min(self.x + self.l, other.x + other.l) - x
        a = max(self.a, other.a)
        w = min(self.a + self.w, other.a + other.w) - a
        return BoundBox(x, l, a, w)


class PipeBox(Box):

    def __init__(self, box_id, x, l, a, w):
        self.box_id = box_id
        super(PipeBox, self).__init__(x, l, a, w)

    def __repr__(self):
        fields = 'id={id},x={x},l={l},a={a},w={w}'.format(id=self.box_id, x=self.x, l=self.l, a=self.a, w=self.w)
        return '<%s [%s]>' % (self.__class__.__name__, fields)

    @property
    def plain_regions(self):
        if self.a + self.w > 360:
            return [BoundBox(self.x, self.l, 0, self.a + self.w - 360),
                    BoundBox(self.x, self.l, self.a, 360 - self.a)]
        else:
            return [BoundBox(self.x, self.l, self.a, self.w)]

    def overlap(self, other, bound_boxes=True):
        """

        Parameters
        ----------
        other : PipeBox
        bound_boxes : bool
            If True use BoundBox instead of PipeBox objects to represent the overlap.

        Returns
        -------
        list[Box]
        """
        overlap = []
        for self_region in self.plain_regions:
            for other_region in other.plain_regions:
                region = self_region.overlap(other_region)
                if region:
                    overlap.append(region)

        # The bound_boxes argument with the following code was added lately as a first step toward using PipeBox as
        # base class to represent also the overlap.
        # The BoundBox could be thrown away and an assert against the a + w > 360 condition could be left only in
        # the testing phase, since the data is made during the computation and doesn't come from outside
        # (in practice unit tests of PipeBox.plain_regions is enough to trust on the data).
        if not bound_boxes and len(overlap) > 1:
            first_box, last_box = overlap[0], overlap[-1]
            if first_box.a == 0 and last_box.a + last_box.w == 360:
                overlap = [self.__class__(None, b.x, b.l, b.a, b.w) for b in overlap[1:-1]]
                overlap.insert(0, self.__class__(None, first_box.x, first_box.l, last_box.a, last_box.w + last_box.a))
        return overlap
