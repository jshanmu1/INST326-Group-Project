# Emilio Sanchez San Martin
# Class

from abc import ABC, abstractmethod

class BaseVisualizer(ABC):
    """
    Abstract base class ensuring there is a required plotting interface.
    Each visualizer subclass has to implement plot_data().
    """

    def __init__(self, dataset):
        self.dataset = dataset   # Composition: Visualizer HAS a Dataset object

    @abstractmethod
    def plot_data(self):
       pass