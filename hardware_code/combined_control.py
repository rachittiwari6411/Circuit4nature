#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os

parser = argparse.ArgumentParser(description='Run robot in manual or autonomous mode')
parser.add_argument('--mode', choices=['manual','auto'], default='auto')
parser.add_argument('--simulate', action='store_true', help='force simulation mode')
args = parser.parse_args()

base = os.path.dirname(os.path.abspath(__file__))
venv_python = sys.executable

if args.mode == 'manual':
    script = os.path.join(base, 'venv', 'wasd_control.py')
else:
    script = os.path.join(base, 'venv', 'main.py')

env = os.environ.copy()
if args.simulate:
    env['SIMULATE'] = '1'

cmd = [venv_python, script]
proc = subprocess.Popen(cmd, env=env)
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    proc.wait()

