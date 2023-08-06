def get_task_name(options):
    """
    Given a dictionary of command options, return the name of the task
    :param options:
    :return:
    """
    options_dict = dict(options)
    return [task for task in [key for key in options_dict] if str(options_dict[task]) == 'True'][0]
