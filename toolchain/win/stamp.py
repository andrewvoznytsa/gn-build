#!/usr/bin/env python3
import sys

def main(path):
  """Simple stamp command."""
  open(path, 'w').close()

if __name__ == '__main__':
  sys.exit(main(*sys.argv[1:]))
