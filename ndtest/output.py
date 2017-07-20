import collections

RESET = '0'
COLOR_NAMES = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
FOREGROUND_COLORS = {COLOR_NAMES[x]: '3%s' % x for x in range(8)}


def color_print(text, fg):
    """ Print text enclosed in ANSI graphics codes.
    Valid colors:
        'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'

    Parameters
    ----------
    text : str
        Text to colorize.
    fg : str
        Foreground color.

    Returns
    -------
    None
    """
    text = '%s\x1b[%sm' % (text or '', RESET)
    print '%s%s' % (('\x1b[%sm' % FOREGROUND_COLORS[fg]), text or '')


def reverse_data(data):
    """ It takes the dictionary returned by `Analyzer.analyse`:
    {
        box_id_new: {
            box_id_old: OverlapMetadata
        }
    }
    and returns a new one where old box ids are swapped with the new ones:
    {
        box_id_old: {
            box_id_new: OverlapMetadata
        }
    }

    Parameters
    ----------
    data : dict[int:dict[int:OverlapMetadata]]

    Returns
    -------
    dict[int:dict[int:OverlapMetadata]]
    """
    new_data = collections.defaultdict(dict)
    for id_box_new in data:
        for id_box_old in data[id_box_new]:
            new_data[id_box_old][id_box_new] = data[id_box_new][id_box_old]
    return dict(new_data)


def _print_results(data, ref_data, sub_data, label):
    sub_data_map = {sub_box.box_id: sub_box for sub_box in sub_data}

    print
    for ref_box in ref_data:
        if ref_box.box_id not in data:
            color_print("New box %s doesn't overlap old boxes!\n" % ref_box, fg='red')
            continue
        length = len(data[ref_box.box_id])
        color_print("%s box %s overlaps %s old %s:\n" %
                    (label.title(), ref_box, length, "boxes" if length > 1 else "box"), fg='green')
        for i, id_box_sub in enumerate(sorted(data[ref_box.box_id])):
            metadata = data[ref_box.box_id][id_box_sub]
            color_print("    %s. %s" % (i + 1, sub_data_map[id_box_sub]), fg='cyan')
            color_print("    ----> percent overlap: new = %.2f %% - old = %.2f %%\n" %
                        (metadata.percent_new, metadata.percent_old), fg='yellow')


def print_results(data, old_data, new_data, reverse=False):
    if reverse:
        _print_results(reverse_data(data), old_data, new_data, 'old')
    else:
        _print_results(data, new_data, old_data, 'new')
