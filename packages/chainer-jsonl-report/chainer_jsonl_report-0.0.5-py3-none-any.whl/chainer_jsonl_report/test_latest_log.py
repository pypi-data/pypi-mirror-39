from .latest_log import LatestLog


def test_update():
    log = LatestLog()
    log.update({'test': 123})
    assert log[0] == {'test': 123}
