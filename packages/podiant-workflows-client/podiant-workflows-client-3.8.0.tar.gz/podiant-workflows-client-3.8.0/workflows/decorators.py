def operation(verbose_name=None, description=None, takes_context=True):
    def wraps(f):
        f._process_name = verbose_name
        f._process_description = description
        f._takes_context = takes_context

        return f

    return wraps
