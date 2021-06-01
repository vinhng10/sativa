import argparse
import yaml
from pathlib import Path

from experiment import Experiment
from utils import get_named_parameters


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

# Get parameter iterator:
parameters = get_named_parameters(
    file_split_size=config.file_split_sizes,
    segment_size=config.segment_sizes,
    thread=config.threads,
    core=config.cores
)

# Run experiment on each parameter setting:
for parameter in parameters:
    experiment = Experiment(
        config.db, file, config.version, config.bucket,
        config.cluster, config.node, config.tool,
        parameter.file_split_size, parameter.segment_size,
        parameter.thread, parameter.cores, auth
    )
    experiment.run()
