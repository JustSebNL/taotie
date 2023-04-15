"""
"""
import os
from threading import Thread

from taotie.gatherer import Gatherer
from taotie.sources.base import BaseSource
from taotie.utils import Logger


class Orchestrator(Thread):
    """The main entry to collect the information from all the sources."""

    def __init__(self, verbose: bool = False):
        super().__init__()
        self.sources = {}
        self.logger = Logger(logger_name=os.path.basename(__file__), verbose=verbose)

    def add_source(self, source: BaseSource):
        self.sources[str(source)] = source

    def set_gatherer(self, gatherer: Gatherer):
        self.gatherer = gatherer

    def run(self):
        if not self.sources:
            self.logger.error("No sources are added.")
            return
        if not self.gatherer:
            self.logger.error("No gatherer is set.")
            return
        for source in self.sources.values():
            source.start()
        self.gatherer.start()
        self.gatherer.join()
        for source in self.sources.values():
            source.join()
