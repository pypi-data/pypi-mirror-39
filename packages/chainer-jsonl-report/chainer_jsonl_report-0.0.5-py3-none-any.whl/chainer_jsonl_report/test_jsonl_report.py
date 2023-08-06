import os
import json
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock
from .jsonl_reporter import JsonlReport


def test_call():
    with TemporaryDirectory() as out:
        report = JsonlReport()
        trainer = MagicMock()
        trainer.out = out
        trainer.elapsed_time = 1000.0
        trainer.observation = {'test': 123}
        trainer.updater.epoch = 1
        trainer.updater.iteration = 100
        trainer.updater.epoch_detail = 1
        trainer.updater.previous_epoch_detail = 0

        report(trainer)
        with open(os.path.join(out, 'log')) as fp:
            log = json.load(fp)

    assert log == {
        'test': 123.0,
        'epoch': 1,
        'iteration': 100,
        'elapsed_time': 1000.0,
    }
