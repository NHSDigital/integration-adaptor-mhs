import abc
from typing import Dict


class RouteLookupClient(abc.ABC):

    @abc.abstractmethod
    async def get_end_point(self, interaction_id: str, ods_code: str = None) -> Dict:
        pass

    @abc.abstractmethod
    async def get_reliability(self, interaction_id: str, ods_code: str = None) -> Dict:
        pass
