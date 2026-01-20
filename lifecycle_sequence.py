#!/usr/bin/env python3
"""Simple helper to drive a lifecycle node through a sequence of transitions

This script uses the `ros2 lifecycle` CLI to request transitions. It is
intended as a lightweight, robust way to automate lifecycle testing without
depending on transition id constants.

Usage:
  python3 lifecycle_sequence.py [node_name]

Example:
  python3 lifecycle_sequence.py motor_driver_lifecycle

Note: this requires a sourced ROS 2 environment so the `ros2` CLI is available.
"""
import subprocess
import time
import sys
from shutil import which

DEFAULT_NODE = 'motor_driver_lifecycle'
STEPS = [
    'configure',
    'activate',
    'deactivate',
    'cleanup',
]


def check_ros2_cli():
    return which('ros2') is not None


def run(cmd):
    print(f'>>> {cmd}')
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.stdout:
        print(p.stdout.strip())
    if p.stderr:
        print(p.stderr.strip(), file=sys.stderr)
    return p.returncode == 0


def main():
    if len(sys.argv) > 1:
        node_name = sys.argv[1]
    else:
        node_name = DEFAULT_NODE

    if not check_ros2_cli():
        print('ERROR: `ros2` CLI not found in PATH. Please source your ROS 2 setup.bash and retry.', file=sys.stderr)
        sys.exit(2)

    print(f'Driving lifecycle for node: {node_name}')

    # show initial state
    run(f'ros2 lifecycle get {node_name}')

    for step in STEPS:
        print('\n---')
        ok = run(f'ros2 lifecycle set {node_name} {step}')
        # show resulting state
        run(f'ros2 lifecycle get {node_name}')
        if not ok:
            print(f'[ERROR] transition `{step}` failed — aborting sequence', file=sys.stderr)
            break
        # short pause so outputs are readable and system has time to settle
        time.sleep(1.0)


if __name__ == '__main__':
    main()
