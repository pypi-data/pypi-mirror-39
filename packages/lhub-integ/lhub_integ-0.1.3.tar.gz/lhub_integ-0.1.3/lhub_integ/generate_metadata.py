"""
`generate_metadata` will load a Python module and generate a metadata JSON that the module
system can use to build an integration descriptor.

Usage:
python -m lhub_integ.generate_metadata
"""
import inspect
import json
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from docstring_parser import parse

from lhub_integ import util, action
from lhub_integ.params import ConnectionParam, ActionParam, DataType, InputType
from lhub_integ.util import print_result


@dataclass
@dataclass_json
class Param:
    id: str
    label: str
    data_type: str
    input_type: str
    optional: bool = False
    description: Optional[str] = None
    default: Optional[str] = None
    options: Optional[List[str]] = None


@dataclass
@dataclass_json
class Action:
    name: str
    entrypoint: str
    args: List[Param]
    params: List[Param]
    description: str
    errors: List[str]


@dataclass
@dataclass_json
class IntegrationMetadata:
    connection_params: List[Param]
    integration_description: str
    actions: List[Action]
    errors: List[str]
    ok: bool


def generate_metadata() -> IntegrationMetadata:
    # Side-effectful action of importing every file in the current working directory.
    # This will populate the internal class-storage for `action`, `ConnectionParam` and `ActionParam`
    toplevel_errors = []
    parse_failure = False
    errors, docstrings = util.import_workdir()
    for error in errors:
        parse_failure = True
        if isinstance(error, SyntaxError):
            toplevel_errors.append(f"Failed to import module: {error}")
        elif isinstance(error, ImportError):
            toplevel_errors.append(
                f"Failed to import module (did you run bundle-integrations?): {error}"
            )
        else:
            toplevel_errors.append(
                f"Failed to import module (Unexpected error): {error}"
            )

    actions = []
    for action_object in action.all().values():
        entrypoint = action_object.entrypoint
        processing_function = action_object.function
        action_name = action_object.name

        # Parse the docstring
        docs = processing_function.__doc__
        parsed = parse(docs)

        errors = []

        # Any docstring on the function itself will be used as the description for the integration
        if parsed.short_description or parsed.long_description:
            function_description = parsed.short_description or parsed.long_description
        else:
            function_description = None

        # Build a map of the actual function arguments to compare with the docstrings
        args, varargs, kwargs = inspect.getargs(processing_function.__code__)
        if varargs:
            errors.append("Varargs are not supported")
        if kwargs:
            errors.append("Kwargs are not supported")

        # default of a label is the id, may update it below when iterating over metadata
        arg_map = {arg: {"id": arg, "label": arg} for arg in args}

        # load labels for column parameters
        for meta in parsed.meta:
            if meta.args[0] == "label" and len(meta.args) == 2:
                arg_map[meta.args[1]]["label"] = meta.description

        # Augment arg_map with information from the docstrings
        for param in parsed.params:
            if param.arg_name not in arg_map:
                errors.append(
                    f"Docstring referenced {param.arg_name} but there were no matching arguments"
                )
            else:
                if param.description is not None:
                    arg_map[param.arg_name]["description"] = param.description
                if param.type_name is not None:
                    arg_map[param.arg_name]["tpe"] = param.type_name

        params = [
            Param(
                id=e.id,
                label=e.label,
                description=e.description,
                default=e.default,
                optional=e.optional,
                data_type=e.data_type.value,
                options=e.options,
                input_type=e.input_type.value,
            )
            for e in ActionParam.for_action(action_object)
        ]
        args = [arg_map[arg] for arg in args]
        args = [
            Param(
                id=arg["id"],
                label=arg["label"],
                description=arg.get("description"),
                data_type=DataType.COLUMN.value,
                input_type=InputType.COLUMN_SELECT.value,
            )
            for arg in args
        ]

        actions.append(
            Action(
                name=action_name,
                entrypoint=entrypoint,
                args=args,
                params=params,
                description=function_description,
                errors=errors,
            )
        )

    connection_params = [
        Param(
            id=e.id,
            label=e.label,
            description=e.description,
            default=e.default,
            optional=e.optional,
            data_type=e.data_type.value,
            options=e.options,
            input_type=e.input_type.value,
        )
        for e in ConnectionParam.all()
    ]

    if not actions and not parse_failure:
        toplevel_errors.append("No actions found. Did you forget to use @action?")

    if docstrings:
        integration_description = docstrings[0].strip()
    elif len(actions) == 1:
        integration_description = actions[0].description
    else:
        integration_description = "No description provided"
    metadata = IntegrationMetadata(
        connection_params=connection_params,
        integration_description=integration_description,
        actions=actions,
        errors=toplevel_errors,
        ok=len(toplevel_errors) == 0,
    )
    return metadata


if __name__ == "__main__":
    import traceback

    try:
        print_result(generate_metadata().to_json())
    except Exception:
        print_result(json.dumps(dict(errors=[traceback.format_exc()])))
        exit(1)
