from pathlib import Path

from utils import (
    AnyPath
)


class SubExperiment:
    def __init__(
        self,
        file: AnyPath,
        version: str,
        bucket: str,
        cluster: str,
        node: str,
        tool: str,
        file_split_size: int,
        segment_size: int,
        thread: int,
        core: int,
        process: int,
        auth: dict
    ):
        self.file = Path(file)
        self.version = version
        self.bucket = bucket
        self.cluster = cluster
        self.node = node
        self.tool = tool
        self.file_split_size = file_split_size
        self.segment_size = segment_size
        self.thread = thread
        self.core = core
        self.process = process
        self.auth = auth

