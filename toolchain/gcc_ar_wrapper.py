#!/usr/bin/env python3
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Runs the 'ar' command after removing its output file first.

This script is invoked like:
  python gcc_ar_wrapper.py --ar=$AR --output=$OUT $OP $INPUTS
to do the equivalent of:
  rm -f $OUT && $AR $OP $OUT $INPUTS
"""

import argparse
import os
import subprocess
import sys
import errno

import wrapper_utils


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--ar',
                      required=True,
                      help='The ar binary to run',
                      metavar='PATH')
  parser.add_argument('--output',
                      required=True,
                      help='Output archive file',
                      metavar='ARCHIVE')
  parser.add_argument('--plugin',
                      help='Load plugin')
  parser.add_argument('--resource-whitelist',
                      help='Merge all resource whitelists into a single file.',
                      metavar='PATH')
  parser.add_argument('operation',
                      help='Operation on the archive')
  parser.add_argument('inputs', nargs='+',
                      help='Input files')
  args = parser.parse_args()

  if args.resource_whitelist:
    whitelist_candidates = wrapper_utils.ResolveRspLinks(args.inputs)
    wrapper_utils.CombineResourceWhitelists(
        whitelist_candidates, args.resource_whitelist)

  command = [args.ar, args.operation]
  if args.plugin is not None:
    command += ['--plugin', args.plugin]
  command.append(args.output)
  command += args.inputs

  # Remove the output file first.
  try:
    os.remove(args.output)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise

  # Now just run the ar command.
  return subprocess.call(wrapper_utils.CommandToRun(command))


if __name__ == "__main__":
  sys.exit(main())
