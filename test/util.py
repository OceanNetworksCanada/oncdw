import logging


def _assert_no_logs(caplog, log_level: int):
    # Sometimes sensor does not have real time data when using duration format,
    # in which case the test will generate a warning log.
    for record in caplog.records:
        assert (
            record.levelno < log_level
        ), f"There should be no {logging.getLevelName(log_level)} and above logs"


def _assert_logs(caplog, log_level: int):
    has_logs = False
    for record in caplog.records:
        if record.levelno == log_level:
            has_logs = True
    assert (
        has_logs
    ), f"There should be at least one {logging.getLevelName(log_level)} log"
