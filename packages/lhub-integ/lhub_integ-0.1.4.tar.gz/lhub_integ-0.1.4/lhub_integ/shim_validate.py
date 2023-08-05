"""
Validate that all the required environment variables have been set to execute this integration. If this fails,
it indicates a bug in the PythonEnvironment machinery. Currently, this doesn't offer the ability for the user to
run custom validations but we could add it here.

eg:

We could look for a method like `module.entrypoint_validate()` and run it. Currently we don't
"""
import inspect
import traceback

import click

from lhub_integ import action, util, connection_validator
from lhub_integ.env import MappedColumnEnvVar
from lhub_integ.params import ConnectionParam, ActionParam
from lhub_integ.util import (
    exit_with_instantiation_errors,
    print_successful_validation_result,
)


@click.command()
@click.option("--entrypoint", "-e", required=False)
@click.option(
    "--validate-connections/--no-validate-connections",
    "check_connections",
    default=False,
)
def main(entrypoint, check_connections):
    validation_errors = []
    try:
        try:
            util.import_workdir()
        except ImportError as ex:
            validation_errors += [{"message": f"Can't import {module_name}: {ex}"}]

        if entrypoint is not None:
            validation_errors += validate_entrypoint(entrypoint)
        if check_connections:
            validation_errors += validate_connections()

    except Exception as ex:
        validation_errors = [
            {
                "message": f"Unexpected exception: {ex}",
                "stack_trace": traceback.format_exc(),
            }
        ]

    if validation_errors:
        exit_with_instantiation_errors(
            1, validation_errors, message="Integration validation failed."
        )
    else:
        print_successful_validation_result()


def validate_connections():
    errors = []
    try:

        for var in ConnectionParam.all():
            if not var.valid():
                errors.append(
                    {"message": "Parameter must be defined", "inputId": var.id}
                )
        if not errors and connection_validator.validator is not None:
            connection_validator.validator()
    except Exception as ex:
        errors += [{"message": str(ex)}]

    return errors


def validate_entrypoint(entrypoint):
    module_name = ".".join(entrypoint.split(".")[:-1])
    function_name = entrypoint.split(".")[-1]

    if module_name == "" or function_name == "":
        return [{"message": "Bad entrypoint format. `Expected filename.functionname`"}]

    # Try to import the world and find the entrypoint

    action_object = action.all().get(entrypoint)
    method = action_object.function
    if method is None:
        return [
            {
                "message": f"No matching action found. Is your action annotated with @action?"
            }
        ]

    errors = []

    # Read the arguments and environment variables we expect and make sure they've all been defined
    args, _, _ = inspect.getargs(method.__code__)
    for arg in args:
        if not MappedColumnEnvVar(arg).valid():
            errors.append({"message": "Column name cannot be empty", "inputId": MappedColumnEnvVar(arg).id})

    env_vars = list(ConnectionParam.all()) + list(ActionParam.for_action(action_object))
    for var in env_vars:
        if not var.valid():
            errors.append({"message": "Parameter cannot be empty", "inputId": var.id})

    if errors:
        return errors

    if action_object.validator is not None:
        try:
            action_object.validator()
        except Exception as ex:
            errors.append({"message": str(ex)})
    return errors


if __name__ == "__main__":
    main()
