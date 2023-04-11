import configparser


def test_configuration_parser():
    config = configparser.ConfigParser()
    config.read('../config.ini')

    debug = config.getboolean('general', 'debug')
    assert debug
    log_file = config.get('general', 'log_file')
    assert log_file == "/var/log/myapp.log"
    db_name = config.get('database', 'name')
    assert db_name == 'szkola'