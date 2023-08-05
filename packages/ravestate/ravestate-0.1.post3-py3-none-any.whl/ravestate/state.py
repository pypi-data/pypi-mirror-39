# Ravestate State-related definitions

import logging
from typing import Callable, Optional, Any


class StateActivationResult:
    """
    Base class for return values of state activation functions.
    """
    pass


class Delete(StateActivationResult):
    """
    Return an instance of this class, if the invoked state should be deleted.
    """
    pass


class Emit(StateActivationResult):
    """
    Return an instance of this class, if the invoked state's signal should be emitted.
    """
    pass


class State:

    action: Callable[[Any], Optional[StateActivationResult]]

    def __init__(self, *, signal, write, read, triggers, action, is_receptor=False):
        assert(callable(action))
        self.name = action.__name__

        # catch the insane case
        if not len(read) and not len(triggers) and not is_receptor:
            logging.warning(
                f"The state `{self.name}` is not reading any properties, nor waiting for any triggers. " +
                "It will never be activated!")

        # convert read/write properties to tuples
        if isinstance(write, str):
            write = (write,)
        if isinstance(read, str):
            read = (read,)

        # listen to default changed-signals if no signals are given.
        # convert triggers to disjunctive normal form.
        if not len(triggers):
            triggers = tuple((f"{rprop_name}:changed",) for rprop_name in read)
        else:
            if isinstance(triggers, str):
                triggers = (triggers,)
            if isinstance(triggers[0], str):
                triggers = (triggers,)

        self.signal = signal
        self.write_props = write
        self.read_props = read
        self.triggers = triggers
        self.action = action
        self.module_name = ""

    def __call__(self, context, args, kwargs) -> StateActivationResult:
        return self.action(context, *args, **kwargs)

    def signal_name(self):
        return f"{self.module_name}:{self.signal}"


def state(*, signal: str="", write: tuple=(), read: tuple=(), triggers: tuple=()):
    """
    Decorator to declare a new state, which may emit a certain signal,
    write to a certain set of properties (calling set, push, pop, delete),
    and read from certain properties (calling read).
    """
    def state_decorator(action):
        nonlocal signal, write, read, triggers
        return State(signal=signal, write=write, read=read, triggers=triggers, action=action)
    return state_decorator
