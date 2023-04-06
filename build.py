#!/usr/bin/env python3

# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

if __name__ != "__main__":
  print("ERROR: this build script cannot be imported as a module")
  exit(1)

import argparse
import os
import sys
import types

# include libdbr in module search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))

from libdbr import config
from libdbr import fileio
from libdbr import logger
from libdbr import paths
from libdbr import tasks


script_name = os.path.basename(sys.argv[0])
logger = logger.getLogger(script_name)

# ~ def printUsage():
  # ~ for key in help_info["options"]:
    # ~ print("key: '{}', value: '{}'".format(key, type(help_info["options"][key])))

def exitWithError(msg, code=1, usage=False):
  if msg:
    logger.error(msg)
  if usage:
    printUsage()
  sys.exit(code)

def checkError(res):
  if res[0] != 0:
    exitWithError(res[1], res[0])

def addTask(name, action, desc):
  tasks.add(name, action)
  task_list[name] = desc


# --- task function --- #

def taskStage():
  tasks.run("clean-stage")

  print()
  logger.info("staging files ...")

  root_stage = paths.join(dir_app, "build/stage")
  root_prefix = paths.join(root_stage, options.prefix)
  root_data = paths.join(root_prefix, "share")
  root_doc = paths.join(root_data, "doc")

  dir_data = paths.join(root_data, package_name)
  dir_doc = paths.join(root_doc, package_name)

  for _dir in config.getValue("dirs_app").split(";"):
    checkError((fileio.copyDir(paths.join(dir_app, _dir), paths.join(dir_data, _dir),
        _filter=r"\.py$", exclude="__pycache__", verbose=options.verbose)))
  for _file in config.getValue("files_doc").split(";"):
    checkError((fileio.copyFile(paths.join(dir_app, _file), paths.join(dir_doc, _file),
        verbose=options.verbose)))

def taskClean():
  tasks.run("clean-stage")

  print()
  logger.info("removing temprary build directory ...")

  dir_build = paths.join(dir_app, "build")
  checkError((fileio.deleteDir(dir_build, verbose=options.verbose)))

def taskCleanStage():
  print()
  logger.info("removing temporary staged build files ...")

  dir_stage = paths.join(dir_app, "build/stage")
  checkError((fileio.deleteDir(dir_stage, verbose=options.verbose)))

def taskRunTests():
  from libdbr.unittest import runTest

  dir_tests = paths.join(dir_app, "tests")
  if not os.path.isdir(dir_tests):
    return

  # add tests directory to module search path
  sys.path.insert(0, dir_tests)
  introspect_tests = {}
  standard_tests = {}

  for ROOT, DIRS, FILES in os.walk(dir_tests):
    for basename in FILES:
      if not basename.endswith(".py") or not basename.startswith("test"):
        continue
      test_file = paths.join(ROOT, basename)
      if os.path.isdir(test_file):
        continue
      test_name = test_file[len(dir_tests)+1:-3].replace(os.sep, ".")
      if test_name.startswith("introspect."):
        introspect_tests[test_name] = test_file
      else:
        standard_tests[test_name] = test_file

  print()
  logger.info("running introspection tests (failure is ok) ...")
  for test_name in introspect_tests:
    # for debugging, it is ok if these tests fail
    res, err = runTest(test_name, introspect_tests[test_name], verbose=options.verbose)
    logger.info("result: {}, message: {}".format(res, err))
  print()
  logger.info("running standard tests ...")
  for test_name in standard_tests:
    res, err = runTest(test_name, standard_tests[test_name], verbose=options.verbose)
    if res != 0:
      exitWithError("{}: failed".format(test_name), res)
    else:
      logger.info("{}: OK".format(test_name))


def initTasks():
  addTask("stage", taskStage, "Prepare files for installation or distribution.")
  addTask("clean", taskClean, "Remove all temporary build files.")
  addTask("clean-stage", taskCleanStage,
      "Remove temporary build files from'build/stage' directory.")
  addTask("test", taskRunTests, "Run configured unit tests from 'tests' directory.")

def initOptions(aparser):
  task_help = []
  for t in task_list:
    task_help.append(t + ": " + task_list[t])

  aparser.version = package_version
  aparser.add_argument("-v", "--version", action="version",
      help="Show libdbr version.")
  aparser.add_argument("-V", "--verbose", action="store_true",
      help="Include detailed task information when printing to stdout.")
  aparser.add_argument("-t", "--task", choices=tuple(task_list),
      help="\n".join(task_help))
  aparser.add_argument("-p", "--prefix", default=paths.getSystemRoot() + "usr",
      help="Path prefix to directory where files are to be installed.")
  aparser.add_argument("-d", "--dir", default=paths.getSystemRoot(),
      help="Target directory (defaults to system root). This is useful for directing the script" \
          + " to place the files in a temporary directory, rather than the intended installation" \
          + " path.")


def main():
  global dir_app
  dir_app = paths.getAppDir()
  config.setFile(paths.join(dir_app, "build.conf"))
  config.load()

  global package_name, package_version
  package_name = config.getValue("package")
  package_version = config.getValue("version")

  # initialize tasks
  global task_list
  task_list = {}
  initTasks()

  # handle command line input
  aparser = argparse.ArgumentParser(
      formatter_class=argparse.RawTextHelpFormatter,
      description="build script for " + config.getValue("package") + ": "
          + config.getValue("description"),
      add_help=True)

  global options
  initOptions(aparser)
  options = aparser.parse_args()

  # set help function
  global printUsage
  printUsage = aparser.print_help

  # override argparse help function
  # ~ global help_info
  # ~ help_info = {
    # ~ "options": aparser.__dict__["_option_string_actions"]
  # ~ }
  # ~ aparser.print_help = printUsage

  global root_install
  root_install = paths.join(options.dir, options.prefix)

  t = tasks.get(options.task)
  if not t:
    exitWithError("unknown task ({})".format(options.task), usage=True)
  if type(t) != types.FunctionType:
    exitWithError("task argument not supplied", usage=True)

  # run task
  err = tasks.run(options.task)
  sys.exit(err)

# execution insertion
main()
