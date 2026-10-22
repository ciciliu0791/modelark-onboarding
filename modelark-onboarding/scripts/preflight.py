#!/usr/bin/env python3
"""Local inventory only: no network, credential reads or installations."""
import argparse
import json
import os
import platform
import re
import shutil
from pathlib import Path


def inspect(workspace):
    roots = [workspace / '.agents/skills', workspace / '.codex/skills',
             Path.home() / '.agents/skills',
             Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills']
    skills = []
    for name in ('seedream', 'seedance', 'volcengine-cli', 'arkcli-shared'):
        for root in roots:
            entry = root / name / 'SKILL.md'
            if not entry.is_file():
                continue
            missing = []
            for link in re.findall(r'\]\(([^)]+)\)', entry.read_text(encoding='utf-8')):
                if not link.startswith(('http:', 'https:', '#', 'skill:')):
                    target = (entry.parent / link.split('#')[0]).resolve()
                    if not target.exists():
                        missing.append(str(target))
            skills.append({'name': name, 'path': str(entry), 'missing_local_references': missing})
    return {'platform': platform.system(), 'python': platform.python_version(),
            'commands': {x: shutil.which(x) for x in ('python3', 'node', 'npm', 've', 'arkcli', 'ffprobe')},
            'skills': skills, 'provider_tools': 'inspect current session tool catalog separately',
            'account_authenticated': 'not_checked', 'generation_ready': 'not_checked'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(inspect(args.workspace.resolve()), ensure_ascii=False, indent=2))
