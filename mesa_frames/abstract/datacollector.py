from abc import ABC,abstractmethod
from typing import Callable, Dict, List, Optional, Union, Any
from agents import ModelDF

class AbstractDataCollector(ABC):

    _model: ModelDF

    def __init__(
        self,
        model: Any,
        model_reporters: Optional[Dict[str, Union[str, Callable]]] = None,
        agent_reporters: Optional[Dict[str, Union[str, Callable]]] = None,
        stats: Optional[Dict[str, Union[List[str], Callable]]] = None,
        trigger: Optional[Callable[[Any], bool]] = None,
        storage: Optional[str] = None
    ):
        self._model = model 
        self._model_reporters = model_reporters or {}
        self._agent_reporters = agent_reporters or {}
        self._stats = stats or {} # confirm if we need this
        self._trigger = trigger or (lambda model: True)
        self._storage_uri = storage or "memory:"
        self._frames = [] 

    def should_collect(self) -> bool:
        """trigger == True"""
        return self._trigger(self._model)

    def collect(self) -> None:
        """ collect if should collect"""
        if self.should_collect():
            self._collect()

    @abstractmethod
    def _collect(self) -> None:
        """ collect data - doesn't materialise until called"""
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """ returns collected data """
        pass

    @abstractmethod
    def flush(self) -> None:
        """if configured persists to external"""
        pass

    @abstractmethod
    def register_stat(self, name: str, func: Callable) -> None:
        """registers a stat"""
        pass

