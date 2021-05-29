import subprocess
from datetime import datetime
from functools import wraps
from pathlib import Path

from utils import (
    AnyPath, Tool, save_to_db,
    upload_file_swift,
    get_network_transfer_rate
)


class SubExperiment:
    def __init__(
        self,
        db: str,
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
        self.core = core
        self.process = process
        self.auth = auth

    def save_file(self) -> None:
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
                self.thread, self.core, self.process, transfer_rate,
                start_time.isoformat(), end_time.isoformat(),
                status
            )
            return result
        return decorated

    @_record_result
    def run(self) -> subprocess.CompletedProcess:
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
        return result
