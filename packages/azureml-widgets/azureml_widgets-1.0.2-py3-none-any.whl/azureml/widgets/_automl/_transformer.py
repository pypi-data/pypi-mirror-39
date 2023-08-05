# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml.widgets._transformer import _DataTransformer


class _AutoMLDataTransformer(_DataTransformer):
    """Transform run and metric data for AutoML runs."""

    def _get_additional_properties(self, run):
        property_bag = run._run_dto['properties']
        top_level_properties = run._run_dto
        goal = property_bag['goal'] if 'goal' in property_bag else None
        run_properties = property_bag['run_properties'] if 'run_properties' in property_bag else None

        if 'run_preprocessor' in property_bag and 'run_algorithm' in property_bag:
            if property_bag['run_preprocessor']:
                run_name = "{0}, {1}".format(property_bag['run_preprocessor'], property_bag['run_algorithm'])
            else:
                run_name = property_bag['run_algorithm']
        else:
            run_name = top_level_properties['status']
        return {
            'iteration': property_bag['iteration'],
            'goal': goal,
            'run_name': run_name,
            'run_properties': run_properties
        }
