import argparse
import yaml
from pathlib import Path

from utils import (
    split_file, save_to_db,
    upload_file_swift
)

##############################################################################
### EXPERIMENT SETUP                                                       ###
##############################################################################

# Parse argument:
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True,
                    help="Path to the file to be transfered.")
parser.add_argument("-a", "--auth", required=True,
                    help="Path to the authentication file.")
parser.add_argument("-c", "--cfg", required=True,
                    help="Path to the experiment config file.")

args = parser.parse_args()

# Read authentication file:
with open(args.auth, "r") as f:
    auth = yaml.load(f, Loader=yaml.FullLoader)

# Read experiment config file:
with open(args.cfg, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Get file path:
file = Path(args.file)

##############################################################################
### EXPERIMENT RUN                                                         ###
##############################################################################

# Save file information to File table:
save_to_db(
    args.db, "File",
    file.name, file.suffix, file.stat().st_size
)

for file_split_size in args.file_split_sizes:
    # Split file into smaller files:
    file_splits = split_file(args.file, file_split_size)

    for segment_size in args.segment_sizes:

        for file_split in file_splits:
            # Save file split information to File table. This is to
            # reuse the result from file split upload:
            save_to_db(
                args.db, "File",
                file_split.name, file_split.suffix, file_split.stat().st_size
            )

            # Perform file upload:
            result = upload_file_swift(
                file_split,
                auth["st_auth_version"],
                auth["os_username"],
                auth["os_password"],
                auth["os_project_name"],
                auth["os_auth_url"],
                config["bucket"],
                segment_size,
                config
            )

            # Check the upload was successful:
            if result.returncode == 0:
                status = "SUCCESSFUL"
            else:
                status = "FAILED"

            transfer_rate = get_transfer_rate()
            transfer_time = get_transfer_time()

            # Save result to Experiment table:
            save_to_db(
                args.db, "Experiment",
                file_split.name, config.version, config.bucket,
                config.cluster, config.node, config.tool,
                file_split_size, segment_size, config.thread,
                config.core, config.process, transfer_rate,
                transfer_time, status
            )

