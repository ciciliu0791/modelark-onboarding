"""Offline checkpoint tests. Dummy assets do not validate real media or provider APIs."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / 'modelark-onboarding/scripts/session.py'


class Checkpoints(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run = self.root / 'run'
        self.call('init')

    def call(self, action, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), action, str(self.run), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return json.loads(result.stdout) if ok else result.stderr

    def finish(self, stage, suffix='.md'):
        artifact = self.root / (stage + suffix)
        artifact.write_text('offline fixture; not valid media')
        return self.call('mark', stage, 'done', '--artifact', str(artifact), '--checked')

    def setup_done(self):
        self.call('begin', 'setup')
        self.finish('setup')

    def test_init_preserves_existing_state(self):
        before = self.call('show')
        self.call('init', ok=False)
        self.assertEqual(before, self.call('show'))

    def test_order_and_completion_evidence(self):
        self.call('begin', 'image', ok=False)
        self.call('begin', 'setup')
        self.call('mark', 'setup', 'done', ok=False)
        empty = self.root / 'empty.md'
        empty.touch()
        self.call('mark', 'setup', 'done', '--artifact', str(empty), '--checked', ok=False)

    def test_pre_submission_wait_can_resume(self):
        self.call('begin', 'setup')
        self.call('mark', 'setup', 'waiting', '--code', 'USER_LOGIN')
        state = self.call('begin', 'setup')
        self.assertEqual(len(state['stages']['setup']['attempts']), 2)

    def test_unknown_outcome_blocks_resubmit(self):
        self.setup_done()
        self.call('begin', 'image')
        self.call('mark', 'image', 'unknown', '--code', 'SUBMISSION_TIMEOUT')
        self.call('begin', 'image', ok=False)
        self.call('mark', 'image', 'waiting', '--code', 'USER_ACTION', ok=False)
        self.call('mark', 'image', 'failed', '--code', 'CONFIRMED_NOT_CREATED')
        state = self.call('begin', 'image')
        self.assertEqual(len(state['stages']['image']['attempts']), 2)

    def test_task_id_is_preserved(self):
        self.setup_done()
        self.call('begin', 'image')
        self.call('mark', 'image', 'running', '--task-id', 'task_123')
        self.call('begin', 'image', ok=False)
        self.call('mark', 'image', 'running', '--task-id', 'task_456', ok=False)
        self.call('mark', 'image', 'waiting', '--code', 'WAIT', ok=False)
        state = self.call('show')
        self.assertEqual(state['stages']['image']['attempts'][0]['task_id'], 'task_123')

    def test_signed_url_rejected_as_task_id(self):
        self.call('begin', 'setup')
        self.call('mark', 'setup', 'running', '--task-id', 'https://example.com?token=secret', ok=False)

    def test_complete_flow_and_no_reopen(self):
        for stage, suffix in [('setup', '.md'), ('image', '.png'), ('video', '.mp4'), ('handoff', '.md')]:
            self.call('begin', stage)
            self.finish(stage, suffix)
            self.call('begin', stage, ok=False)
        state = self.call('show')
        self.assertTrue(all(item['status'] == 'done' for item in state['stages'].values()))
        self.assertEqual((self.run / 'onboarding-state.json').stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()
