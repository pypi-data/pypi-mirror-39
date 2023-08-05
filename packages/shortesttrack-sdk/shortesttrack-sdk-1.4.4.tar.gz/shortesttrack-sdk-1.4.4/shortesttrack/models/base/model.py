from shortesttrack.conf.library import ULibrary


class Model:
    _id_key = 'id'

    def __init__(self, metadata: dict, *args, **kwargs) -> None:
        self._metadata = metadata
        self._id = metadata[self._id_key]
        self._lib = ULibrary

    @property
    def metadata(self) -> dict:
        return self._metadata

    @property
    def id(self) -> str:
        return self._id
