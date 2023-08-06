from shortesttrack import constants
from shortesttrack.models import Matrix
from shortesttrack.models.base.model import Model
from shortesttrack_tools.logger.utils import get_prototype_logger

logger = get_prototype_logger('performance')


class Performance(Model):
    def __str__(self) -> str:
        return f'Performance({self.id})'

    def send_success(self) -> None:
        path = f'v1/sec/{self._lib.script_configuration.id}/performances/{self.id}/success/'
        self._lib.exec_scheduler_endpoint.request(self._lib.exec_scheduler_endpoint.POST, path, raw_content=True)

    def send_failed(self) -> None:
        path = f'v1/sec/{self._lib.script_configuration.id}/performances/{self.id}/failed/'
        self._lib.exec_scheduler_endpoint.request(self._lib.exec_scheduler_endpoint.POST, path, raw_content=True)

    def write_parameter(self, parameter_id: str, parameter_value: str or list or dict,
                        parameter_type: str = constants.TYPE_DEFAULT) -> None:
        """
        Write OutputParameter to Performance
        """
        path = f'performances/{self.id}/output-parameters/{parameter_id}/value/'
        body = {
            'value': parameter_value,
            'parameter_type': parameter_type
        }
        self._lib.exec_api_endpoint.request(self._lib.exec_api_endpoint.POST, path, json=body, raw_content=True)

    def write_result(self, model: Model) -> None:
        """
        Attach model object as a Performance output parameter
        """
        if isinstance(model, Matrix):
            self.write_parameter(
                parameter_id=model.name,
                parameter_value=model.metadata,
                parameter_type=constants.TYPE_RESULT_MATRIX
            )
            return

        try:
            from shortesttrack.models.dataset import Dataset
        except ImportError:
            logger.warning(f'Fix Dataprovider client import side effect')
            return

        if isinstance(model, Dataset):
            self.write_parameter(
                parameter_id=model.name,
                parameter_value=model.metadata,
                parameter_type=constants.TYPE_RESULT_DATASET
            )
            return

        logger.info(f'Skip writing result: unsupported type {type(model)} for {model}')
