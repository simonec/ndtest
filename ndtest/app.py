import loader
import inspection
import output


def ndtest(old_path, new_path, reverse):
    """ Collate new inspection with an old one and print to the standard output a result report.

    Parameters
    ----------
    old_path : str
    new_path : str
    reverse : bool

    Returns
    -------
    None
    """
    old_data, new_data = loader.load(old_path), loader.load(new_path)

    data = inspection.Collator.analyze(old_data, new_data)
    output.print_results(data, old_data, new_data, reverse)
