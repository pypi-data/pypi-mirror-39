import pytest
import logging
from logging import getLogger, DEBUG, INFO
import filecmp
import pathlib
from os import path

from corautil.corautil import CoraUtil

base_dir = path.dirname(__file__)


@pytest.mark.parametrize(('station_name', 'filename'),
                         [
                             ('Framingham_Interchange_13_South', 's3621_framingham-13-south_das-1.CR8'),
                             ('Framingham_Interchange_13_South', 's3621_framingham-13-south.cfg'),
                             # ('Framingham_Interchange_13_South', '.draker_id')
                         ]
                         )
def test_get_file(station_name, filename):
    logger = getLogger('test_get_file')
    logger.setLevel(DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logger.addHandler(console)

    loggernet = CoraUtil('devops.inaccess.com', '', '')
    loggernet.set_logger_level(DEBUG)

    loggernet.get_file(station_name, filename)

    assert filecmp.cmp(filename, filename + '.orig')
