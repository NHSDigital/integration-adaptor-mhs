import abc
from typing import Dict


class RouteLookupClient(abc.ABC):

    @abc.abstractmethod
    async def get_end_point(self, service_id: str, org_code: str = None) -> Dict:
        pass

    @abc.abstractmethod
    async def get_reliability(self, service_id: str, org_code: str = None) -> Dict:
        pass
