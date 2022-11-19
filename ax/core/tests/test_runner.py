#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from unittest import mock

from ax.core.base_trial import BaseTrial
from ax.core.runner import Runner
from ax.utils.common.testutils import TestCase
from ax.utils.testing.core_stubs import get_trial, get_batch_trial


class DummyRunner(Runner):
    def run(self, trial: BaseTrial):
        return {"metadatum": f"value_for_trial_{trial.index}"}


class RunnerTest(TestCase):
    def setUp(self):
        self.dummy_runner = DummyRunner()
        self.trials = [get_trial(), get_batch_trial()]

    def test_base_runner_staging_required(self):
        self.assertFalse(self.dummy_runner.staging_required)

    def test_base_runner_stop(self):
        with self.assertRaises(NotImplementedError):
            self.dummy_runner.stop(trial=mock.Mock(), reason="")

    def test_base_runner_clone(self):
        runner_clone = self.dummy_runner.clone()
        self.assertIsInstance(runner_clone, DummyRunner)
        self.assertEqual(runner_clone, self.dummy_runner)

    def test_base_runner_run_multiple(self):
        metadata = self.dummy_runner.run_multiple(trials=self.trials)
        self.assertEqual(
            metadata,
            {t.index: {"metadatum": f"value_for_trial_{t.index}"} for t in self.trials},
        )
        self.assertEqual({}, self.dummy_runner.run_multiple(trials=[]))

    def test_base_runner_poll_trial_status(self):
        with self.assertRaises(NotImplementedError):
            self.dummy_runner.poll_trial_status(trials=self.trials)

    def test_poll_available_capacity(self):
        self.assertEqual(self.dummy_runner.poll_available_capacity(), -1)
