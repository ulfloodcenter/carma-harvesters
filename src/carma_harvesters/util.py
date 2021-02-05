import subprocess
import logging
import os


OGR_PREFIX = os.environ.get('OGR_PREFIX', '/usr')


logger = logging.getLogger(__name__)


class Geometry:
    """
    Wrap GeoJSON-like object so that it can be used in tools like Shapely, for example:
    ```
    from shapely.geometry import asShape
    s = asShape(Geometry(object))
    ```
    """
    def __init__(self, object):
        self.__geo_interface__ = object


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
