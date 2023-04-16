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
import errno
import os
import re
import subprocess
import sys
import types

# include libdbr in module search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))

from libdbr         import config
from libdbr         import fileio
from libdbr         import misc
from libdbr         import paths
from libdbr         import tasks
from libdbr.logger  import LogLevel
from libdbr.logger  import Logger
from libdbr.strings import sgr


script_name = os.path.basename(sys.argv[0])
logger = Logger(script_name)

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
  tasks.run(("update-version", "clean-stage"))

  print()
  logger.info("staging files ...")

  root_stage = paths.join(dir_app, "build/stage")
  root_prefix = paths.join(root_stage, options.prefix)
  root_data = paths.join(root_prefix, "share")
  root_doc = paths.join(root_data, "doc")

  dir_data = paths.join(root_data, package_name)
  dir_doc = paths.join(root_doc, package_name)

  for _dir in cfg.getValue("dirs_app").split(";"):
    checkError((fileio.copyDir(paths.join(dir_app, _dir), paths.join(dir_data, _dir),
        _filter=r"\.py$", exclude="__pycache__", verbose=options.verbose)))
  for _file in cfg.getValue("files_doc").split(";"):
    checkError((fileio.copyFile(paths.join(dir_app, _file), paths.join(dir_doc, _file),
        verbose=options.verbose)))

def taskDistSource():
  tasks.run("clean-stage")

  print()
  logger.info("building source distribution package ...")

  root_stage = paths.join(dir_app, "build/stage")
  root_dist = paths.join(dir_app, "build/dist")

  for _dir in cfg.getValue("dirs_dist_py").split(";"):
    abspath = paths.join(dir_app, _dir)
    checkError((fileio.copyDir(abspath, paths.join(root_stage, _dir), exclude=r"^(.*\.pyc|__pycache__)$", verbose=options.verbose)))
  for _dir in cfg.getValue("dirs_dist_data").split(";"):
    abspath = paths.join(dir_app, _dir)
    checkError((fileio.copyDir(abspath, paths.join(root_stage, _dir), verbose=options.verbose)))
  for _file in cfg.getValue("files_dist_data").split(";"):
    abspath = paths.join(dir_app, _file)
    checkError((fileio.copyFile(abspath, paths.join(root_stage, _file), verbose=options.verbose)))
  for _file in cfg.getValue("files_dist_exe").split(";"):
    abspath = paths.join(dir_app, _file)
    checkError((fileio.copyExecutable(abspath, paths.join(root_stage, _file), verbose=options.verbose)))

  pkg_dist = paths.join(root_dist, package_name + "_" + package_version_full + ".tar.xz")

  # FIXME: parent directory should be created automatically
  if not os.path.isdir(root_dist):
    fileio.makeDir(root_dist, verbose=options.verbose)

  checkError((fileio.packDir(root_stage, pkg_dist, form="xz", verbose=options.verbose)))

  if os.path.isfile(pkg_dist):
    logger.info("built package '{}'".format(pkg_dist))
  else:
    exitWithError("failed to build source package", errno.ENOENT)

def taskBuildDocs():
  tasks.run("update-version")

  print()
  logger.info("building Doxygen documentation ...")

  dir_docs = paths.join(dir_app, "build/docs")
  fileio.makeDir(dir_docs, verbose=options.verbose)
  subprocess.run(["doxygen"])
  logger.info("cleaning up ...")
  for ROOT, DIRS, FILES in os.walk(paths.join(dir_docs, "html")):
    for _file in FILES:
      if not _file.endswith(".html"):
        continue
      abspath = paths.join(ROOT, _file)
      fileio.replace(abspath, r"^<!DOCTYPE html.*>$", "<!DOCTYPE html>", count=1, flags=re.M)

def __cleanByteCode(_dir):
  if os.path.basename(_dir) == "__pycache__":
    checkError((fileio.deleteDir(_dir, verbose=options.verbose)))
    return
  for obj in os.listdir(_dir):
    abspath = paths.join(_dir, obj)
    if os.path.isdir(abspath):
      __cleanByteCode(abspath)
    elif obj.endswith(".pyc") and os.path.lexists(abspath):
      checkError((fileio.deleteFile(abspath, verbose=options.verbose)))

def taskClean():
  tasks.run(("clean-stage", "clean-dist"))

  print()
  logger.info("removing build directory ...")

  dir_build = paths.join(dir_app, "build")
  checkError((fileio.deleteDir(dir_build, verbose=options.verbose)))

  excludes = cfg.getValue("exclude_clean_dirs").split(";")
  for ROOT, DIRS, FILES in os.walk(dir_app):
    for _dir in DIRS:
      abspath = paths.join(ROOT, _dir)
      relpath = abspath[len(dir_app)+1:]
      if re.match(r"^({})".format("|".join(excludes)), relpath, flags=re.M):
        continue
      __cleanByteCode(abspath)

def taskCleanStage():
  print()
  logger.info("removing temporary staged build files ...")

  dir_stage = paths.join(dir_app, "build/stage")
  checkError((fileio.deleteDir(dir_stage, verbose=options.verbose)))

def taskCleanDist():
  print()
  logger.info("removing built distribution packages ...")

  dir_dist = paths.join(dir_app, "build/dist")
  checkError((fileio.deleteDir(dir_dist, verbose=options.verbose)))

def taskUpdateVersion():
  print()
  print("package:     {}".format(package_name))
  print("version:     {}".format(package_version_full))

  print()
  logger.info("updating version information ...")

  file_doxy = paths.join(dir_app, "Doxyfile")
  fileio.replace(file_doxy, r"^PROJECT_NUMBER(.*?)=.*$",
      r"PROJECT_NUMBER\1= {}".format(package_version_full), count=1, flags=re.M)
  # update changelog for non-development versions only
  if package_version_dev == 0:
    fileio.replace(paths.join(dir_app, "doc/changelog.txt"), r"^next$", package_version_full,
        count=1, fl=True, verbose=options.verbose)
  tmp = package_version.split(".")
  script_main = paths.join(dir_app, "lib/libdbr/__init__.py")
  fileio.replace(script_main, r"^version_major = .*$", "version_major = {}".format(tmp[0]),
      count=1, verbose=options.verbose)
  fileio.replace(script_main, r"^version_minor = .*$", "version_minor = {}".format(tmp[1]),
      count=1, verbose=options.verbose)
  fileio.replace(script_main, r"^version_dev = .*$", "version_dev = {}".format(package_version_dev),
      count=1, verbose=options.verbose)

def taskRunTests():
  from libdbr.unittest import runTest

  # enable debugging for tests
  Logger.setLevel(LogLevel.DEBUG)

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

def taskCheckCode():
  print()
  for action in ("pylint", "mypy"):
    logger.info("checking code with {} ...".format(action))
    params = [action, dir_app]
    if options.verbose:
      params.insert(1, "-v")
    res = subprocess.run(params)
    if res.returncode != 0:
      return res.returncode

def taskPrintChanges():
  changelog = paths.join(paths.getAppDir(), "doc/changelog.txt")
  if not os.path.isfile(changelog):
    return
  print(misc.getLatestChanges(changelog))


def initTasks():
  addTask("stage", taskStage, "Prepare files for installation or distribution.")
  addTask("dist-source", taskDistSource, "Build a source distribution package.")
  addTask("docs", taskBuildDocs, sgr("Build documentation using <bold>Doxygen</bold>."))
  addTask("clean", taskClean, "Remove all temporary build files.")
  addTask("clean-stage", taskCleanStage,
      "Remove temporary build files from 'build/stage' directory.")
  addTask("clean-dist", taskCleanDist, "Remove built packages from 'build/dist' directory.")
  addTask("update-version", taskUpdateVersion,
      "Update relevant files with version information from 'build.conf'.")
  addTask("test", taskRunTests, "Run configured unit tests from 'tests' directory.")
  addTask("check-code", taskCheckCode, "Check code with pylint & mypy.")
  addTask("changes", taskPrintChanges,
      "Print most recent changes from 'doc/changelog.txt' to stdout.")

def initOptions(aparser):
  task_help = []
  for t in task_list:
    task_help.append(t + ": " + task_list[t])

  log_levels = []
  for level in LogLevel.getLevels():
    log_levels.append(sgr("<bold>{}) {}</bold>").format(level, LogLevel.toString(level).lower()))

  aparser.add_argument("-v", "--version", action="store_true",
      help="Show libdbr version.")
  aparser.add_argument("-V", "--verbose", action="store_true",
      help="Include detailed task information when printing to stdout.")
  aparser.add_argument("-l", "--log-level", metavar="<level>",
      default=LogLevel.toString(LogLevel.getDefault()).lower(),
      help="Logging output verbosity.\n  " + "\n  ".join(log_levels))
  aparser.add_argument("-t", "--task", #choices=tuple(task_list),
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

  # ensure current working directory is app location
  os.chdir(dir_app)

  # initialize tasks
  global task_list
  task_list = {}
  initTasks()

  # handle command line input
  aparser = argparse.ArgumentParser(
      formatter_class=argparse.RawTextHelpFormatter,
      description="build script for libdbr",
      add_help=True)

  global options
  initOptions(aparser)
  options = aparser.parse_args()

  err = LogLevel.check(options.log_level)
  if isinstance(err, Exception):
    sys.stderr.write(sgr("<red>ERROR: {}</fg>\n".format(err)))
    print()
    aparser.print_help()
    exit(1)

  # set logger level before calling config functions
  logger.setLevel(options.log_level)

  global cfg
  cfg = config.add("build", paths.join(dir_app, "build.conf"))

  global package_name, package_version, package_version_dev, package_version_full
  package_name = cfg.getValue("package")
  package_version = cfg.getValue("version")
  package_version_dev = 0
  tmp = cfg.getValue("version_dev")
  if tmp:
    package_version_dev = int(tmp)
  package_version_full = package_version
  if package_version_dev > 0:
    package_version_full = "{}-dev{}".format(package_version_full, package_version_dev)
  aparser.version = package_version_full

  # set help function
  global printUsage
  printUsage = aparser.print_help

  if options.version:
    print(aparser.version)
    exit(0)

  # override argparse help function
  # ~ global help_info
  # ~ help_info = {
    # ~ "options": aparser.__dict__["_option_string_actions"]
  # ~ }
  # ~ aparser.print_help = printUsage

  global root_install
  root_install = paths.join(options.dir, options.prefix)

  if not options.task:
    exitWithError("task argument not supplied", usage=True)
  t_ids = options.task.split(",")
  # check all request task IDs
  for _id in t_ids:
    if not _id in task_list:
      exitWithError("unknown task ({})".format(options.task), usage=True)
  # run tasks
  for _id in t_ids:
    err = tasks.run(_id)
    if err != 0:
      sys.exit(err)

# execution insertion
main()
