from corautil.corautil import CoraUtil

import pytest
from logging import getLogger, DEBUG, INFO


@pytest.mark.parametrize(('station_name', 'filename'),
                         [
                             ('Framingham_Interchange_13_North', 'CoServ_SolarStation'),
                             ('currentProgramName', 89),
                         ]
                         )
def test_get_file(station_name, filename):
    logger = getLogger('test_get_file')
    logger.setLevel(DEBUG)

    loggernet = CoraUtil('devops.inaccess.com', '', '')
    loggernet.set_logger_level(DEBUG)

    loggernet.get_file(station_name, filename)
