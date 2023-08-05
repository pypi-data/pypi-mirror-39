# flake8: noqa
from esroofit.version import version as __version__
from esroofit.exceptions import *

try:
    import ROOT
except ImportError:
    from esroofit import MissingRootError

    raise MissingRootError()

try:
    from ROOT import RooFit
except ImportError:
    try:
        # noinspection PyUnresolvedReferences
        import ROOT.RooFit
    except ImportError:
        from esroofit import MissingRooFitError

        raise MissingRooFitError()

try:
    from ROOT import RooStats
except ImportError:
    try:
        # noinspection PyUnresolvedReferences
        import ROOT.RooStats
    except ImportError:
        from esroofit import MissingRooStatsError

        raise MissingRooStatsError()

from esroofit import decorators
from esroofit.roofit_manager import RooFitManager
