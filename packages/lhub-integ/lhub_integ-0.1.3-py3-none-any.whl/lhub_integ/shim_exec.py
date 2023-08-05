"""
Wrap a custom Python script to enable it to work with the integration machinery

Loads ENTRYPOINT from `__ENTRYPOINT` and the column-argument mapping from `___XXXXX`

Usage:
This module is intended to be invoked by `PythonEnvironment`. See `test_shim.py` for a usage example

<set required environment variables> python -m lhub_integ.shim_exec -e <entrypoint>
"""
import json
import sys
import traceback

import click

from lhub_integ import util, action
from lhub_integ.env import MappedColumnEnvVar


def run_integration(entrypoint_fn):
    type_mapper = util.get_input_converter(entrypoint_fn)

    # Build a mapping from the columns in the input data to the arguments in our integration
    argument_column_mapping = {
        input_argument: MappedColumnEnvVar(input_argument).read()
        for input_argument in type_mapper
    }

    for row in sys.stdin.readlines():
        as_dict = json.loads(row)["row"]
        lhub_id = as_dict.get(util.LHUB_ID)
        missing_keys = argument_column_mapping.values() - as_dict.keys()
        for column in missing_keys:
            util.print_error(f"Column '{column}' is not present in the data")
        if missing_keys:
            continue
        try:

            # Load the arguments from the input
            arguments = {
                arg: type_mapper[arg](as_dict[column])
                for arg, column in argument_column_mapping.items()
            }

            # Run the integration
            result = entrypoint_fn(**arguments)

            # Print the results
            if result:
                if isinstance(result, list):
                    util.print_each_result_in_list(result, lhub_id)
                else:
                    util.print_result(json.dumps(result), lhub_id)
        except Exception:
            util.print_error(traceback.format_exc(), data=as_dict)


@click.command()
@click.option("--entrypoint", "-e", required=True)
def main(entrypoint):
    util.import_workdir()
    entrypoint_fn = action.all().get(entrypoint).function
    assert entrypoint_fn is not None
    run_integration(entrypoint_fn)


if __name__ == "__main__":
    main()
