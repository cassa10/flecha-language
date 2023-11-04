import argparse

from config import Config
from flecha.execution.package import Execution
from flecha.execution.repl import REPL

if __name__ == "__main__":
    # Get config and input arguments
    config_and_inputs = Config(argparse.ArgumentParser())

    if config_and_inputs.run_repl:
        REPL().run()
    else:
        Execution(config_and_inputs).execute()
