import json

from shortesttrack_tools.logger.utils import get_prototype_logger

from shortesttrack import constants
from shortesttrack.client import ISSConnector
from shortesttrack.models import Matrix
from shortesttrack.models.base.model import Model

__all__ = ['ISSConnectionInfo', 'AnalyticScriptConfiguration']

logger = get_prototype_logger('analytic-script-configuration')


class BatchAnalysisException(Exception):
    pass


class ISSConnectionInfo:
    # TODO: move to a separate model IterativeService
    def __init__(self, info: dict) -> None:
        self.url = info.get('url')
        self.url = self.url if self.url[-1] != '/' else self.url[0:-1]
        self.auth_custom_token = info.get('auth_custom_token')
        self.id = info.get('iscript_service_id')


class AnalyticScriptConfiguration(Model):
    _id_key = 'uuid'

    # Custom for analysis_type = batch
    _reference_matrix: Matrix = None
    _result_matrix: Matrix = None

    def __init__(self, metadata: dict) -> None:
        super().__init__(metadata)

        self.analysis_type = str(metadata.get('analysis_type')).lower()
        self._batch_analysis_data = self.metadata.get('analysis_performance_config', {})

    def __str__(self) -> str:
        return f'ASEC({self.id})'

    @property
    def batch(self) -> bool:
        return self.analysis_type == constants.ANALYSIS_TYPE_BATCH

    @property
    def batch_analysis_data(self) -> dict:
        if not self.batch:
            return {}

        return self._batch_analysis_data

    @property
    def _reference_matrix_id(self) -> str or None:
        return self.batch_analysis_data.get('reference_matrix_id')

    @property
    def _result_matrix_id(self) -> str or None:
        return self.batch_analysis_data.get('result_matrix_id')

    @property
    def _reference_field_name(self) -> str:
        return self.batch_analysis_data.get('reference_field_name')

    @property
    def _result_field_name(self) -> str:
        return self.batch_analysis_data.get('result_field_name')

    @property
    def reference_matrix(self) -> Matrix or None:
        if not self._reference_matrix_id:
            return None

        if self._reference_matrix:
            return self._reference_matrix

        self._reference_matrix = Matrix(metadata={'matrixId': self._result_matrix_id}).read()
        return self._reference_matrix

    @property
    def result_matrix(self) -> Matrix or None:
        if not self._result_matrix_id:
            return None

        if self._result_matrix:
            return self._result_matrix

        self._result_matrix = Matrix(metadata={'matrixId': self._result_matrix_id}).read()
        return self._result_matrix

    @property
    def reference_column(self) -> list:
        if not self.reference_matrix:
            raise BatchAnalysisException(f'Cannot get reference column: {self.batch_analysis_data}')

        if not self._reference_field_name:
            raise BatchAnalysisException(f'Empty reference field name: {self.batch_analysis_data}')

        index = self.reference_matrix.fields.index(self._reference_field_name)
        return self.reference_matrix.get_column(index)

    @property
    def result_column(self) -> list:
        if not self.result_matrix:
            raise BatchAnalysisException(f'Cannot get reference column: {self.batch_analysis_data}')

        if not self._result_field_name:
            raise BatchAnalysisException(f'Empty reference field name: {self.batch_analysis_data}')

        index = self.result_matrix.fields.index(self._result_field_name)
        return self.result_matrix.get_column(index)

    def get_iss_connection_info(self) -> list:
        return [ISSConnectionInfo(info) for info in self.metadata.get('relations', [])]

    @staticmethod
    def get_iss_connector(connection_info: ISSConnectionInfo) -> ISSConnector:
        return ISSConnector(
            url=connection_info.url, auth_custom_token=connection_info.auth_custom_token
        )

    def write_result(self, result: dict) -> None:
        if not self._lib.performance:
            logger.error(f'Cannot write analytic result: no performance metadata found {self._lib.performance}')
            return

        self._lib.performance.write_parameter(
            parameter_id='analysis_result',
            parameter_value=result,
            parameter_type=constants.TYPE_ANALYSIS_RESULT
        )
