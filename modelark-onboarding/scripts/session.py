#!/usr/bin/env python3
"""Single-writer local onboarding checkpoints; never calls a provider."""
import argparse
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STAGES = ('setup', 'image', 'video', 'handoff')
STATES = ('pending', 'running', 'waiting', 'unknown', 'failed', 'done')


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, state):
    state['updated_at'] = now()
    fd, name = tempfile.mkstemp(prefix='.state-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(state, out, ensure_ascii=False, indent=2)
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def apply(state, action, stage, status=None, task_id=None, artifact=None, checked=False, code=None):
    item = state['stages'][stage]
    if action == 'begin':
        if item['status'] in ('running', 'unknown', 'done'):
            raise ValueError('Existing attempt must be reconciled; cannot resubmit or reopen completed work')
        previous = STAGES[:STAGES.index(stage)]
        if any(state['stages'][p]['status'] != 'done' for p in previous):
            raise ValueError('Complete prior stages before beginning this stage')
        item['attempts'].append({'started_at': now(), 'status': 'running', 'task_id': None})
        item['status'] = 'running'
        return
    if not item['attempts'] or item['status'] not in ('running', 'unknown'):
        raise ValueError('Only an in-flight or unresolved attempt may be marked')
    attempt = item['attempts'][-1]
    if status == 'waiting' and (attempt['task_id'] or item['status'] == 'unknown'):
        raise ValueError('Submitted or unknown outcome must remain in-flight until reconciled')
    if status == 'done':
        if not checked or not artifact:
            raise ValueError('Completion requires an artifact and an explicit verification attestation')
        p = Path(artifact).resolve()
        if not p.is_file() or p.stat().st_size == 0:
            raise ValueError('Completion artifact must be an existing nonempty local file')
        allowed = {'image': ('.png', '.jpg', '.jpeg', '.webp'),
                   'video': ('.mp4', '.mov', '.webm'),
                   'setup': ('.md',), 'handoff': ('.md',)}
        if p.suffix.lower() not in allowed[stage]:
            raise ValueError('Artifact format does not match this stage')
        attempt['artifact'] = str(p)
        attempt['verification'] = 'agent_attested; helper checked file existence only'
    if task_id:
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', task_id):
            raise ValueError('Use a provider resource ID, never a URL or secret')
        if attempt['task_id'] and attempt['task_id'] != task_id:
            raise ValueError('Cannot replace an existing provider ID in the same attempt')
        attempt['task_id'] = task_id
    if code:
        if not re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}', code):
            raise ValueError('Use a short uppercase category, not raw logs or credentials')
        attempt['code'] = code
    if status in ('waiting', 'failed', 'unknown') and not code:
        raise ValueError('Waiting/failure/unknown states require a reason code')
    attempt['status'] = item['status'] = status
    attempt['updated_at'] = now()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('init', 'show', 'begin', 'mark'))
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('stage', nargs='?', choices=STAGES)
    parser.add_argument('status', nargs='?', choices=STATES[1:])
    parser.add_argument('--task-id')
    parser.add_argument('--artifact')
    parser.add_argument('--checked', action='store_true')
    parser.add_argument('--code')
    args = parser.parse_args()
    root = args.run_dir.resolve()
    path = root / 'onboarding-state.json'
    if args.action == 'init':
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        state = {'schema_version': 1, 'created_at': now(),
                 'stages': {s: {'status': 'pending', 'attempts': []} for s in STAGES}}
        # Exclusive creation prevents a repeated init from erasing progress.
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise ValueError('Run already exists; use show to resume')
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(state, out, ensure_ascii=False, indent=2)
    else:
        state = json.loads(path.read_text(encoding='utf-8'))
        if state.get('schema_version') != 1:
            raise ValueError('Unsupported state schema; do not overwrite')
        if args.action != 'show':
            if not args.stage or (args.action == 'mark' and not args.status):
                raise ValueError('begin requires a stage; mark requires a stage and status')
            apply(state, args.action, args.stage, args.status, args.task_id,
                  args.artifact, args.checked, args.code)
            save(path, state)
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(str(error))
