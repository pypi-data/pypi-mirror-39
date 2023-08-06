from shortesttrack_tools.functional import cached_property

from shortesttrack.models.base.model import Model


class Matrix(Model):
    _id_key = 'matrixId'
    _content = None

    def __init__(self, metadata: dict, *args, **kwargs) -> None:
        super().__init__(metadata, args, kwargs)
        self._metadata['name'] = self.name

    def __str__(self) -> str:
        return f'Matrix({self.id})'

    @property
    def name(self) -> str:
        return self.metadata.get('name') or self.metadata.get('id') or 'unknown'

    @property
    def filled(self) -> bool:
        return bool(self._content)

    @property
    def data(self) -> dict:
        return self._content['matrix']

    @cached_property
    def fields(self) -> list:
        return [f['name'] for f in self._content['fields']]

    def read(self) -> 'Matrix':
        self._content = self.get_matrix(self.id)
        return self

    def insert(self, fields: list or dict, matrix_data: list) -> None:
        fields = [f['name'] for f in fields] if isinstance(fields, dict) else fields
        self.insert_matrix(self.id, fields, matrix_data)

    # Moved from SECHelper
    def get_matrix(self, matrix_id: str) -> dict:
        matrix_raw = self._lib.data_endpoint.get_matrix(matrix_id)
        return self.matrix_from_api_format_to_sdk_content(matrix_raw)

    @staticmethod
    def matrix_from_api_format_to_sdk_content(json_data: dict) -> dict:
        """
        Convert matrix data from data-api format:
            rows: [
                0: {f: [{v: "1"}, {v: "2"}]}
                1: {f: [{v: "3"}, {v: "4"}]}
            ]

        to SDK format:
            [
                [1, 2],
                [3, 4]
            ]
        """
        fields = json_data['schema']['fields']
        matrix = [
            [
                v.get('v') for v in f.get('f', [])
            ] for f in json_data.get('rows', [])
        ]
        return dict(
            fields=fields,
            matrix=matrix
        )

    @staticmethod
    def matrix_from_sdk_content_to_api_format(content: dict) -> dict:
        """
        Convert matrix data from SDK format:
            [
                [1, 2],
                [3, 4]
            ]
        to data-api format:
            rows: [
                0: {f: [{v: "1"}, {v: "2"}]}
                1: {f: [{v: "3"}, {v: "4"}]}
            ]
        """
        insert_rows = []
        for row in content.get('matrix'):
            tmp = {}
            for field, v in zip(content['fields'], row):
                tmp[field] = v
            insert_rows.append({"json": tmp})

        return dict(rows=insert_rows)

    def insert_matrix(self, matrix_id: str, fields: list, data: list) -> None:
        matrix_sdk_content = dict(matrix=data, fields=fields)
        matrix_raw = self.matrix_from_sdk_content_to_api_format(matrix_sdk_content)
        self._lib.data_endpoint.insert_matrix(matrix_id, matrix_raw)

        if self._lib.performance:
            self._lib.performance.write_result(self)

    def get_column(self, index: int) -> list:
        return [row[index] for row in self.data]
