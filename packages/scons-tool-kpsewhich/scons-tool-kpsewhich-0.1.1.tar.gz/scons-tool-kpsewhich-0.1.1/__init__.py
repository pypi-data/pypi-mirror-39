"""kpsewhich tool

Tool-specific initialization for kpsewhich.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013 The SCons Foundation
# Copyright (c) 2013-2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

from .about import __version__

class _Missing(object): pass
_missing = _Missing

_argnames = [ 'dpi', 'format', 'path', 'progname', 'subdir' ]


def _kwargs2flags(env, allowed = _missing, **kw):
    import SCons.Util
    global _argnames;

    flags = SCons.Util.CLVar([])

    if allowed is _missing:
        # All the flags from _argnames are allowed
        args = [x for x in _argnames if x in kw]
    else:
        # Only some flags are allowed
        args = [x for x in _argnames if x in allowed and x in kw]

    for arg in args:
        f = "-%s" % str(arg).replace('_','-')
        v = env.subst(kw[arg])
        flags += SCons.Util.CLVar([f, v])

    return flags

def _kpsewhich(env, args, allowed = _missing, **kw):
    """Workhorse for all KPSXxx methods"""
    import SCons.Util
    import subprocess
    import sys

    kps = env.get('KPSVARIABLES', dict())
    kps.update(kw.get('KPSVARIABLES', dict()))

    env = env.Override(kw)
    ENV = env.get('ENV', dict())
    ENV.update(kps)

    # Workaround for kpsewhich bug - first file is not found when -path is
    # used, this is due to recursive use of non-reentrant functions within
    # the kpathsea library.
    if kw.get('_findfiles'):
        ENV['_KPS_VV_WKND_'] = "$_KPS_VV_WKND_VALUE"
        prepend = SCons.Util.CLVar(['-var-value', '_KPS_VV_WKND_'])
    else:
        prepend = SCons.Util.CLVar([])

    flags = _kwargs2flags(env, allowed, **kw)

    exe = env.WhereIs('$KPSEWHICH') or env.subst('$KPSEWHICH')
    cmd = SCons.Util.CLVar(exe) \
        + SCons.Util.CLVar(env.subst('$KPSEWHICHFLAGS')) \
        + prepend + flags + SCons.Util.CLVar(args)

    kw2 = {'env': ENV}
    if sys.version_info < (3,7):
        kw2['universal_newlines'] = True
    else:
        kw2['text'] = True
    out = subprocess.check_output(cmd, **kw2).rstrip('\r\n')

    if kw.get('_findfiles'):
        out = "\n".join(out.splitlines()[1:])
    return out

def KPSFindFiles(env, files, **kw):
    """Find files using ``kpsewhich`` program.

    The keyword parameters correspond to the options of ``kpsewhich`` program.
    See ``kpsewhich`` manual and `kpathsea`_ documentation.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:

        env
            the SCons Environment object,
        files
            the list of file names (strings)

    :Keywords:

        dpi
            base resolution,
        format
            string, file type to use,
        path
            search in the given path,
        progname
            set program name (e.g. latex, jadetex, etc.), this may affect search
        subdir
            only output matches whose directory ends with ``subdir``

    :Returns:

        list of absolute paths to files

    .. _kpathsea: http://tug.org/texinfohtml/kpathsea.html
    """
    output = _kpsewhich(env, files, _findfiles=True, **kw)
    result = output.splitlines()
    return result

def KPSFindAllFiles(env, files, **kw):
    """Find files as in `KPSFindFiles` but with ``-all`` command-line flag."""
    import SCons.Util
    args = SCons.Util.CLVar('-all') + SCons.Util.CLVar(files)
    output = _kpsewhich(env, args, _findfiles=True, **kw)
    result = output.splitlines()
    return result

def KPSExpandBraces(env, string, **kw):
    """Return variable and brace expansion of string from ``kpsewhich``
    program.

    This function simply returns the output of ``kpsewhich ... -expand-braces
    <string>`` command.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:
        env
            the SCons Environment object,
        string
            the string to be expanded
    :Keywords:
        progname
            set program name (e.g. latex, jadetex, etc.)
    :Returns:
        the expanded ``string``
    """
    return _kpsewhich(env, ['-expand-braces', string], ['progname'], **kw)

def KPSExpandPath(env, string, **kw):
    """Return complete path expansion of string from ``kpsewhich`` program

    This function simply returns the output of ``kpsewhich ... -expand-path
    <string>`` command.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:
        env
            the SCons Environment object,
        string
            the string to be expanded
    :Keywords:
        progname
            set program name (e.g. latex, jadetex, etc.)
    :Returns:
        the expanded ``string``
    """
    return _kpsewhich(env, ['-expand-path', string], ['progname'], **kw)

def KPSExpandVar(env, string, **kw):
    """Return variable expansion of string from ``kpsewhich`` program

    This function simply returns the output of ``kpsewhich ... -expand-var
    <string>`` command.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:
        env
            the SCons Environment object,
        string
            the string to be expanded
    :Keywords:
        progname
            set program name (e.g. latex, jadetex, etc.)
    :Returns:
        the expanded ``string``
    """
    return _kpsewhich(env, ['-expand-var', string], ['progname'],**kw)

def KPSShowPath(env, ftype, **kw):
    """Return search path for given file type from ``kpsewhich`` program

    This function simply returns the output of ``kpsewhich ... -show-path
    <ftype>`` command.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:
        env
            the SCons Environment object,
        ftype
            the file type,
    :Keywords:
        progname
            set program name (e.g. latex, jadetex, etc.)
    :Returns:
        the expanded ``string``
    """
    return _kpsewhich(env, ['-show-path', ftype], ['progname'], **kw)

def KPSVarValue(env, varname, **kw):
    """Return the value of variable ``varname`` from ``kpsewhich`` program

    This function simply returns the output of ``kpsewhich ... -var-value
    <varname>`` command.

    Note: in addition to parameters mentioned below, the method also accepts
    construction variables ``KPSEWHICH``, ``KPSEWHICHFLAGS``, ``KPSVARIABLES``.

    :Parameters:
        env
            the SCons Environment object,
        varname
            name of the variable to be returned,
    :Keywords:
        progname
            set program name (e.g. latex, jadetex, etc.)
    :Returns:
        the expanded ``string``
    """
    return _kpsewhich(env, ['-var-value', varname], ['progname'],**kw)

_KPSGenerated = False

def generate(env):
    """Add KPSXxx methods to the environment."""

    import SCons.Util
    global _KPSGenerated
    if _KPSGenerated: return

    kpsewhich = env.Detect(['kpsewhich'])
    if not kpsewhich: kpsewhich = 'kpsewhich'

    env.SetDefault( KPSEWHICH = kpsewhich,
                    KPSEWHICHFLAGS = SCons.Util.CLVar([]),
                    KPSEWHICHCHDIR = '.')

    env.AddMethod(KPSFindFiles, 'KPSFindFiles')
    env.AddMethod(KPSFindAllFiles,'KPSFindAllFiles')
    env.AddMethod(KPSExpandBraces,'KPSExpandBraces')
    env.AddMethod(KPSExpandPath,'KPSExpandPath')
    env.AddMethod(KPSExpandVar,'KPSExpandVar')
    env.AddMethod(KPSShowPath,'KPSShowPath')
    env.AddMethod(KPSVarValue,'KPSVarValue')

    _KPSGenerated = True


def exists(env):
    return env.Detect('kpsewhich')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
