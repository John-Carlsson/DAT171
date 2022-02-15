
""" Python module with useful printing functions!
Author: Emilia Emilsson (2020-2021), emiemi@chalmers.se """

version = "0.0.1" # Module global variable


def print_two_objects(object1, object2):
    """Prints the two objects to stdout.

    :param object1: The first object to print
    :type object1: Any type convertible to str

    :param object2: The second object to print
    :type object2: Any type convertible to str
    """
    print(f'The two objects are: "{object1}" and "{object2}".')

    
def task_done():
    """Indicate that a task is done by printing a message."""
    print('Task done.')
