import argparse
import json
from pathlib import Path

from experiment import Experiment
from utils import get_parameters_dicts


##############################################################################
### EXPERIMENT SETUP                                                       ###
##############################################################################

# Parse argument:
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True,
                    help="Path to the file to be transfered.")
parser.add_argument("-c", "--cfg", required=True,
                    help="Path to the experiment config file.")

args = parser.parse_args()

# Read experiment config file:
with open(args.cfg, "r") as f:
    config = json.load(f)

# Get file path:
file = Path(args.file)

##############################################################################
### EXPERIMENT RUN                                                         ###
##############################################################################

# Get parameter iterator:
parameters = get_parameters_dicts(
    file_split_size=config["file_split_sizes"],
    segment_size=config["segment_sizes"],
    thread=config["threads"],
    core=config["cores"]
)

# Run experiment on each parameter setting:
for parameter in parameters:
    print(f"Run experiment with {parameter} ...")

    experiment = Experiment(
        config["db"], file, config["version"], config["bucket"],
        config["cluster"], config["node"], config["tool"],
        parameter["file_split_size"], parameter["segment_size"],
        parameter["thread"], parameter["core"]
    )

    results = experiment.run()

    experiment.delete_bucket()

    print("Finished experiment.\n")
