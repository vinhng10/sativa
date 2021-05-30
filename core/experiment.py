import subprocess
from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
from multiprocessing import Pool
from pathlib import Path
from typing import List

from utils import (
    AnyPath, Tool, save_to_db,
    upload_file_swift, upload_file_s3cmd, upload_file_rclone,
    split_file, get_network_transfer_rate
)


class BaseExperiment(ABC):
    def __init__(self, db: str, file: AnyPath, version: str,
                 bucket: str, cluster: str, node: str, tool: str,
                 file_split_size: int, segment_size: int,
                 thread: int, cores: int, auth: dict):
        self.db = db
        self.file = Path(file)
        self.version = version
        self.bucket = bucket
        self.cluster = cluster
        self.node = node
        self.tool = tool
        self.file_split_size = file_split_size
        self.segment_size = segment_size
        self.thread = thread
        self.cores = cores
        self.auth = auth

    def record_file(self) -> None:
        save_to_db(
            self.db, "File",
            self.file.name, self.file.suffix, self.file.stat().st_size
        )

    def _record_result(f):
        """"""
        @wraps(f)
        def decorated(self, *args, **kwargs):
            start_time = datetime.now()
            result = f(self, *args, **kwargs)
            end_time = datetime.now()

            # Check the status of the function:
            if result.returncode == 0:
                status = "SUCCESSFUL"
            else:
                print(result.stderr)
                status = "FAILED"

            # Get network transfer rate:
            transfer_rate = get_network_transfer_rate()

            # Record the result to database:
            save_to_db(
                self.db, "Experiment",
                self.file.name, self.version, self.bucket,
                self.cluster, self.node, self.tool,
                self.file_split_size, self.segment_size,
                self.thread, self.cores, transfer_rate,
                start_time.isoformat(), end_time.isoformat(),
                status
            )
            return result
        return decorated

    @abstractmethod
    @_record_result
    def run(self) -> None:
        ...


class SubExperiment(BaseExperiment):
    def __init__(self, db: str, file: AnyPath, version: str,
                 bucket: str, cluster: str, node: str, tool: str,
                 file_split_size: int, segment_size: int,
                 thread: int, cores: int, auth: dict) -> None:
        super().__init__(db, file, version, bucket, cluster,
                         node, tool, file_split_size, segment_size,
                         thread, cores, auth)

    def run(self) -> subprocess.CompletedProcess:
        # Record file information to the database:
        self.record_file()

        # Run file transfer using specified tool:
        if self.tool == Tool.SWIFT.value:
            result = upload_file_swift(
                self.file,
                self.auth["st_auth_version"],
                self.auth["os_username"],
                self.auth["os_password"],
                self.auth["os_project_name"],
                self.auth["os_auth_url"],
                self.bucket,
                self.segment_size,
                self.thread
            )
        elif self.tool == Tool.S3CMD.value:
            result = upload_file_s3cmd()
        elif self.tool == Tool.RCLONE.value:
            result = upload_file_rclone()

        return result


class Experiment(BaseExperiment):
    def __init__(self, db: str, file: AnyPath, version: str,
                 bucket: str, cluster: str, node: str, tool: str,
                 file_split_size: int, segment_size: int,
                 thread: int, cores: int, auth: dict) -> None:
        super().__init__(db, file, version, bucket, cluster,
                         node, tool, file_split_size, segment_size,
                         thread, cores, auth)

    def run_sub_experiment(self, file: Path) -> subprocess.CompletedProcess:
        sub_experiment = SubExperiment(
            self.db, file, self.version, self.bucket, self.cluster,
            self.node, self.tool, self.file_split_size, self.segment_size,
            self.thread, 1, self.auth
        )
        result = sub_experiment.run()
        return result

    def run(self) -> List[subprocess.CompletedProcess]:
        # Record file information to the database:
        self.record_file()

        # Split file into smaller files for parallel transfer:
        split_files = split_file(
            file=self.file,
            file_split_size=self.file_split_size,
            file_split_chunk=self.cores
        )

        # Spawn a pool of workers to process transfer:
        with Pool(self.cores) as pool:
            results = pool.map(self.run_sub_experiment, split_files)

        return results




