"""
Module with official **emloop** hooks.


.. tip::

    Hooks listed here may be configured without specifying their fully qualified names. E.g.:

    .. code-block:: yaml

        hooks:
          - SaveBest

"""
from .abstract_hook import AbstractHook, TrainingTerminated
from .every_n_epoch import EveryNEpoch
from .accumulate_variables import AccumulateVariables
from .write_csv import WriteCSV
from .stop_after import StopAfter
from .log_variables import LogVariables
from .log_profile import LogProfile
from .log_dir import LogDir
from .save import SaveEvery, SaveBest, SaveLatest
from .compute_stats import ComputeStats
from .check import Check
from .show_progress import ShowProgress
from .on_plateau import OnPlateau
from .stop_on_plateau import StopOnPlateau
from .stop_on_nan import StopOnNaN
from .save_cm import SaveConfusionMatrix
from .flatten import Flatten
from .plot_lines import PlotLines
from .logits_to_csv import LogitsToCsv
from .sequence_to_csv import SequenceToCsv
from .save_file import SaveFile

AbstractHook.__module__ = '.hooks'

__all__ = ['AbstractHook', 'TrainingTerminated', 'AccumulateVariables', 'WriteCSV', 'StopAfter', 'LogVariables',
           'LogProfile', 'LogDir', 'SaveEvery', 'SaveBest', 'SaveLatest', 'ComputeStats', 'Check', 'ShowProgress',
           'EveryNEpoch', 'OnPlateau', 'StopOnPlateau', 'StopOnNaN', 'SaveConfusionMatrix', 'Flatten', 'PlotLines',
           'LogitsToCsv', 'SequenceToCsv', 'SaveFile']

