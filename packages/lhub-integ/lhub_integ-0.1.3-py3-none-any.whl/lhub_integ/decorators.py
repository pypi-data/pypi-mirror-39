from lhub_integ import util

"""
You can annotate a function with either @action or @action("action name"). 
Adding a name will set the name, otherwise it will default to the entrypoint. 
Part of the hairiness is from accepting both versions since they have totally different 
"""


class action:
    actions = {}

    # add_action is called by all code paths for an action
    def add_action(self, f):
        # See https://www.python.org/dev/peps/pep-3155/
        if f.__name__ != f.__qualname__:
            util.exit_with_instantiation_errors(
                code="invalid_action", errors=["actions must be top level functions"]
            )

        self.function = f
        self.entrypoint = f"{f.__module__}.{f.__name__}"
        if not self.name:
            self.name = self.entrypoint
        self.actions[self.entrypoint] = self

    def __init__(self, name=None, validator=None):
        # these will be set in add_action
        self.function = None
        self.entrypoint = None
        self.name = None
        self.validator = None

        # if the first argument is callable, the first argument is actually the function
        if name and callable(name):
            self.add_action(name)
        # otherwise we're in the @action(string) case where the given argument is the name
        else:
            self.name = name
            self.validator = validator

    def __call__(self, f, *args, **kwargs):
        # if @action case __call__ is called when the function is called, act as only a pass-through
        if self.function:
            self.function(f, *args, **kwargs)
        # in the @action(string) case __call__ is called with the function itself and should return a function
        else:
            if not f:
                util.exit_with_instantiation_errors(
                    code="invalid_action",
                    errors=["@action is not called with a function"],
                )
            else:
                self.add_action(f)
                return f

    @classmethod
    def all(cls):
        return cls.actions


class connection_validator:
    validator = None

    def __init__(self, f):
        self.f = f
        if connection_validator.validator is not None:
            util.exit_with_instantiation_errors(
                code="too_many_validators",
                errors=[
                    "Only one function can be annotated with @connection_validator"
                ],
            )
        connection_validator.validator = self

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)
