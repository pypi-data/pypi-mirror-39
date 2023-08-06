from dataprovider_client import Client

from shortesttrack.utils import getLogger
from shortesttrack.models.base.model import Model

logger = getLogger()


class Dataset(Model):
    _id_key = 'id'
    _content = None

    def __init__(self, metadata, *args, **kwargs):
        super().__init__(metadata, args, kwargs)
        # {'addr': 'localhost:50051'}
        self._client = Client(
            self._lib.config.dataprovider
        )

    def __str__(self) -> str:
        return f'Dataset({self.id})'

    @property
    def name(self):
        return self.metadata[self._id_key]

    @property
    def datasource_id(self) -> str:
        return self.metadata['datasource_id']

    def read(self) -> list:
        try:
            return list(self._client.read(dataset_id=self.id, datasource_id=self.datasource_id))
        except self._client.DataproviderClientException:
            logger.exception(f'Cannot read from {self}')
            raise

    def write(self, rows: [tuple]) -> None:
        try:
            self._client.write(data=rows, dataset_id=self.id, datasource_id=self.datasource_id)
        except self._client.DataproviderClientException:
            logger.exception(f'Cannot write {len(rows)} rows into {self}')
            raise

        if self._lib.performance:
            self._lib.performance.write_result(self)
