from .bootstrap.executive_office import ExecutiveOffice
from .bootstrap.legislative_office import LegislativeOffice
from .bootstrap.special_election import SpecialElection
from .bootstrap.general_election import GeneralElection


class BootstrapContentMethods(
    ExecutiveOffice, LegislativeOffice, SpecialElection, GeneralElection
):
    pass
