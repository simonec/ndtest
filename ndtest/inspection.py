import collections


class OverlapMetadata(object):
    """ A simple  class to hold overlapping metadata between a new box and an old one. """

    def __init__(self, id_old, id_new, overlaps, percent_old, percent_new):
        """
        Parameters
        ----------
        id_old : int
            Id of the old box.
        id_new : int
            Id of the new box
        overlaps : list[Box]
            List of the overlapping boxes.
        percent_old : int/float
            Percent of overlapped area of the old box.
        percent_new : int/float
            Percent of overlapped area of the new box.
        """
        self.id_old = id_old
        self.id_new = id_new
        self.overlaps = overlaps
        self.percent_old = percent_old
        self.percent_new = percent_new

    def __repr__(self):
        return "<{name} [id_old={id_old},id_new={id_new},percent_old={percent_old},percent_new={percent_new}]>".format(
            name=self.__class__.__name__, id_old=self.id_old, id_new=self.id_new,
            percent_old=self.percent_old, percent_new=self.percent_new)


class Analyzer(object):
    """ It takes to list of boxes coming from inspections and """

    CONTINUE = "CONTINUE"
    BREAK = "BREAK"
    PASS = "PASS"

    @classmethod
    def _prompt_statement(cls, old_box, new_box):
        if old_box.x + old_box.l <= new_box.x:
            # <TEST>test_analysis__new_after_old_along_x__empty</TEST>
            #
            # Because of the sorting applied by `loader.load` we have to continue the cycle along the old data,
            # since we are sure that later boxes in the cycle are closer than the current.
            return cls.CONTINUE

        if new_box.a + new_box.w > 360:
            if old_box.a >= new_box.a + new_box.w - 360 and old_box.a + old_box.w <= new_box.a:
                # <TEST>test_analysis__new_circular_vs_old_plain__middle</TEST>
                #
                # A portion of old box lies in the empty space between the bottom and the top of new box.
                return cls.CONTINUE
                # <TEST>test_analysis__new_circular_vs_old_plain__down</TEST>
                # <TEST>test_analysis__new_circular_vs_old_plain__up</TEST>
        elif old_box.a + old_box.w <= new_box.a:
            # <TEST>test_analysis__new_after_old_along_a__empty</TEST>
            #
            # We have to skip old_box because it doesn't overlap with new_box.
            # However, because of the sorting applied by `loader.load` we must continue the cycle since
            # next items will be closer in terms of x and (after of) a.
            return cls.CONTINUE

        if new_box.x + new_box.l <= old_box.x:
            # <TEST>test_analysis__old_after_new_along_x__empty</TEST>
            #
            # Because of the sorting applied by `loader.load` we can now break the cycle along the old data,
            # since we are sure that later boxes in the cycle are further away in the pipeline.
            return cls.BREAK

        if old_box.a + old_box.w > 360:
            if new_box.a >= old_box.a + old_box.w - 360 and new_box.a + new_box.w <= old_box.a:
                # <TEST>test_analysis__old_circular_vs_new_plain__middle</TEST>
                #
                # A portion of new box lies in the empty space between the bottom and the top of old box.
                return cls.CONTINUE
                # <TEST>test_analysis__old_circular_vs_new_plain__down</TEST>
                # <TEST>test_analysis__old_circular_vs_new_plain__up</TEST>
        elif new_box.a + new_box.w <= old_box.a:
            # <TEST>test_analysis__old_after_new_along_a__empty</TEST>
            #
            # We have to skip old_box because it doesn't overlap with new_box.
            # However, because of the sorting applied by `loader.load` we must continue the cycle since
            # next items will be closer in terms of x and (after of) a.
            return cls.CONTINUE

        return cls.PASS

    @classmethod
    def analyze(cls, old_data, new_data):
        """ It implements the algorithm target of the test and returns a dictionary whose keys are box ids of the new
        inspection while values are dictionaries whose keys are box ids of the old inspection which values are
        `OverlapMetadata` objects who describe the overlap between the pairs box_id_new -> box_id_old pointing to
        each of the those objects.

        Parameters
        ----------
        old_data : list[PipeBox]
            List of boxes from an old inspection - list[PipeBox]
        new_data : list[PipeBox]
            List of boxes from a new inspection - list[PipeBox]

        Returns
        -------
        dict[int:dict[int:OverlapMetadata]]

            In practice, it returns a dictionary like:

            {
                box_id_new: {
                    box_id_old: OverlapMetadata
                }
            }

        """
        analysis_data = collections.defaultdict(dict)
        for new_box in new_data:
            for old_box in old_data:

                statement = cls._prompt_statement(old_box, new_box)
                if statement == cls.BREAK:
                    break
                elif statement == cls.CONTINUE:
                    continue

                overlaps = old_box.overlap(new_box)
                if overlaps:
                    overlap_area = sum(o.area() for o in overlaps)
                    new_percent = overlap_area / new_box.area() * 100
                    old_percent = overlap_area / old_box.area() * 100
                    metadata = OverlapMetadata(new_box.box_id, old_box.box_id, overlaps, old_percent, new_percent)
                    analysis_data[new_box.box_id][old_box.box_id] = metadata
        return analysis_data
