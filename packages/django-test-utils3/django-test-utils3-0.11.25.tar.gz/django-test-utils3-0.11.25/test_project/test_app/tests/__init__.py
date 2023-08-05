from .assertions_tests import *
from .templatetags_tests import *
from .testmaker_tests import *
from .crawler_tests import *

from . import twill_tests

__test__ =  {
'TWILL': twill_tests,
}
