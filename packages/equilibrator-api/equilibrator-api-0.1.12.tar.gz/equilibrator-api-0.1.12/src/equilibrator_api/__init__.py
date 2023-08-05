from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .component_contribution import ComponentContribution
from .reaction import Reaction
from .compound import Compound
from .pathway import Pathway
from .reaction_matcher import ReactionMatcher
from .reaction_matcher import CompoundMatcher
from .query_parser import QueryParser, ParseError
from .bounds import Bounds

