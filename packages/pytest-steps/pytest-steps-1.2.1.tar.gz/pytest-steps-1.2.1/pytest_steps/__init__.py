from sys import version_info as vi
if vi >= (3, 0):
    # Python 3+: load all the symbols with 'more explicit api'
    from pytest_steps.steps_py3_api import test_steps, depends_on
else:
    from pytest_steps.steps import test_steps
    from pytest_steps.steps_parametrizer import depends_on

from pytest_steps.steps_generator import optional_step, one_per_step
from pytest_steps.steps_parametrizer import StepsDataHolder
from pytest_steps.steps_harvest import handle_steps_in_synthesis_dct, remove_step_from_test_id, \
    get_all_pytest_param_names_except_step_id
from pytest_steps.steps_harvest_df_utils import pivot_steps_on_df, get_flattened_multilevel_columns

__all__ = [
    # the submodules
    'steps', 'decorator_hack', 'steps_common', 'steps_generator', 'steps_parametrizer', 'steps_harvest',
    # all symbols imported above
    'test_steps',
    'StepsDataHolder', 'depends_on',
    'optional_step', 'one_per_step',
    'handle_steps_in_synthesis_dct', 'remove_step_from_test_id', 'get_all_pytest_param_names_except_step_id',
    'pivot_steps_on_df', 'get_flattened_multilevel_columns'
]
