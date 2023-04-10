
<a name="top">
<h1>libdbr</h1>
</a>


<a name="toc">
<h2>Contents</h2>
</a>

- [Description](#description)
- [Licensing](#license)
- [Building](#build)
    - [Build Script Options](#build-script-args)
    - [Build Script Tasks](#build-script-tasks)
- [Links](#links)


<a name="description">
<h2><a href="#toc">Description</a></h2>
</a>

A high level Python library for [Debreate][].


<a name="license">
<h2><a href="#toc">Licensing</a></h2>
</a>

libdbr is licensed under [MIT](LICENSE.txt).


<a name="build">
<h2><a href="#toc">Building</a></h2>
</a>

A `build.py` script is provided to help with installation & packaging. It is invoked as
`python3 build.py [args]` or `./build.py [args]`.


<a name="build-script-args">
<h3><a href="#toc">Build Script Options</a></h3>
</a>

- `-h|--help`
    - Show help information.
- `-v|--version`
    - Show libdbr version.
- `-V|--verbose`
    - Include detailed task information when printing to stdout.
- `-t|--task <task>`
    - Task(s) to execute. Multiple tasks can be separated by comma. See
      [Build Script Tasks](#build-script-tasks).
- `-p|--prefix <path>`
    - Path prefix to directory where files are to be installed.
- `-d|--dir <path>`
    - Target directory (defaults to system root). This is useful for directing the script to place
      the files in a temporary directory, rather than the intended installation path. It is
      equivalent to the "[DESTDIR][bs.gnu-destdir]" environment variable used by
      [GNU make][bs.gnu-make].


<a name="build-script-tasks">
<h3><a href="#toc">Build Script Tasks</a></h3>
</a>

- `stage`
    - Prepare files for installation or distribution.
- `dist-source`
    - Build a source distribution package.
- `clean`
    - Remove all temporary build files.
- `clean-stage`
    - Remove temporary build files from'build/stage' directory.
- `clean-dist`
    - Remove built packages from 'build/dist' directory.
- `test`
    - Run configured unit tests from 'tests' directory.
- `check-code`
    - Check code with [pylint][proj.pylint] & [mypy][].


<a name="links">
<h3><a href="#toc">Links</a></h3>
</a>

- [libdbr on GitHub][proj.libdbr]
- [libdbr on GitLab][proj.libdbr.gl]
- [libdbr on SourceForge][proj.libdbr.sf]
- [debreate on GitHub][proj.debreate]
- [debreate on GitLab][proj.debreate.gl]
- [debreate on SourceForge][proj.debreate.sf]
- [reference](https://debreate.github.io/libdbr/reference/)


<!-- project pages -->
[proj.debreate]: https://github.com/debreate/debreate
[proj.debreate.gl]: https://gitlab.com/debreate/debreate
[proj.debreate.sf]: https://sourceforge.net/projects/debreate
[proj.libdbr]: https://github.com/debreate/libdbr
[proj.libdbr.gl]: https://gitlab.com/debreate/libdbr
[proj.libdbr.sf]: https://sourceforge.net/p/debreate/libdbr
[proj.pylint]: https://github.com/pylint-dev/pylint

<!-- home pages -->
[Debreate]: https://debreate.github.io/
[mypy]: https://mypy-lang.org/

<!-- bs: Build System -->
[bs.gnu-destdir]: https://www.gnu.org/prep/standards/html_node/DESTDIR.html
[bs.gnu-make]: https://www.gnu.org/software/make/
