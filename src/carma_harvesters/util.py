import subprocess
import logging
import os


OGR_PREFIX = os.environ.get('OGR_PREFIX', '/usr/local')


logger = logging.getLogger(__name__)


def run_cmd(cmd: str, *args):
    cmd = [cmd]
    cmd.extend(args)
    cmd_str = ' '.join(cmd)
    logger.debug(f"Running {cmd_str}...")
    p = subprocess.Popen(cmd_str, shell=True)
    p.wait()
    logger.debug(f"Command {cmd_str} returned {p.returncode}")
    if p.returncode != 0:
        raise Exception(f"Command {cmd_str} failed with return code {p.returncode}")


def run_ogr2ogr(*args) -> int:
    return run_cmd(f"{OGR_PREFIX}/bin/ogr2ogr", *args)
