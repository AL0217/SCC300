"""Registry keeping track of all registered pluggable components"""

# Dictionary storying all strategy implementations keyed by ID
STRATEGY = {}

# Dictionary storying all network topologies keyed by ID
TOPOLOGY_FACTORY = {}


def register_decorator(register):
    """Returns a decorator that register a class or function to a specified
    register

    Parameters
    ----------
    register : dict
        The register to which the class or function is register

    Returns
    -------
    decorator : func
        The decorator
    """

    def decorator(name):
        """Decorator that register a class or a function to a register.

        Parameters
        ----------
        name : str
            The name assigned to the class or function to store in the register
        """

        def _decorator(function):
            register[name] = function
            function.name = name
            return function

        return _decorator

    return decorator


register_strategy = register_decorator(STRATEGY)
register_topology_factory = register_decorator(TOPOLOGY_FACTORY)
