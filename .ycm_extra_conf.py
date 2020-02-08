import os
import subprocess
import logging

from collections import OrderedDict

logger = logging.getLogger('ycm_extra_conf_logger')

logger.setLevel(logging.DEBUG)

SOURCE_EXTENSIONS = ['.cc', '.cpp', '.c']
HEADER_EXTENSIONS = ['.h', '.hpp', '.hh']

# Which dirs to check for a corresponding source file
CXX_CORRESPONDING_SRC_FILE_DIR = ['/', '/../cpp/']

def GetUserName():
    return os.getlogin()


def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS


def FindCorrespondingSourceFile(filename):
    if IsHeaderFile(filename):
        logger.debug('Finding source file for %s' % filename)
        basename = os.path.splitext(filename)[0]
        for extension in SOURCE_EXTENSIONS:
            for d in CXX_CORRESPONDING_SRC_FILE_DIR:
                replacement_file = os.path.dirname(filename) + d + os.path.splitext(os.path.basename(filename))[0] + extension
                logger.debug('Checking potential source file location %s' % replacement_file)
                if os.path.exists(replacement_file):
                    logger.debug('Found source file')
                    return replacement_file
    return filename


def GetPythonInterpreterPath(filename):
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return ''
    venvpath = basename + '/build/functional_test/venv/bin/python'
    if os.path.exists(venvpath):
        return venvpath
    return ''


def GetPythonSitePackages(filename):
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return ''
    sitepackages = basename + '/build/functional_test/venv/lib/python3.7/site-packages'
    if os.path.exists(sitepackages):
        return sitepackages
    return ''


def Settings(**kwargs):
    filename = kwargs['filename']
    language = kwargs['language']

    if not filename.startswith('/home/%s' % GetUserName()):
        logger.debug('Tried to get settings for %s, ignoring' % filename)
        return {}

    if language == 'cfamily':
        filename = FindCorrespondingSourceFile(filename)
        code_file_no_ext = os.path.splitext(os.path.basename(filename))[0]

        release_env_dirname = os.path.dirname(filename)
        makefile_dirname = os.path.dirname(filename)

        while release_env_dirname != '/home/%s' % GetUserName() and \
                not os.path.exists(release_env_dirname + '/release/env'):
            release_env_dirname = os.path.dirname(release_env_dirname)
            if os.path.exists(release_env_dirname + '/Makefile'):
                makefile_dirname = release_env_dirname

        if release_env_dirname == '/home/%s' % GetUserName():
            logger.debug('Could not find release/env script')
            return {}

        makefile_path = makefile_dirname + '/Makefile'
        if not os.path.exists(makefile_path):
            logger.debug('Could not find Makefile')
            return {}

        cmds = [
            'cd %s' % release_env_dirname,
            'source ./release/env',
            'source $GRADLE_ATSPLUGINS_HOME/bin/setup-build-env',
            'cd %s' % makefile_dirname,
            'make -n %s.o | grep %s.o | tr -d "\\n" | tr -d "\\t"' % (\
                    code_file_no_ext, code_file_no_ext),
            'echo " --sysroot=$CHROOT_HOME"'
        ]
        

        cmd_out = subprocess.Popen(";".join(cmds), shell=True, \
                stdout=subprocess.PIPE).stdout.read()

        if len(cmd_out) == 0:
            logger.debug('Cmd returned empty output')
            return {}

        cxx_flags = ['-x', 'c++', '-g', '-DUSE_CLANG_COMPLETER', '-DYCM_EXPORT=']
        cxx_flags.extend(cmd_out.strip().split(' ')[3:])

        logger.debug(cxx_flags)

        return {
            'flags': cxx_flags,
            'override_filename': filename
        }
    elif language == 'python':
        return {
            'interpreter_path': GetPythonInterpreterPath(filename),
            'sys_path': [
                GetPythonSitePackages(filename)
            ]
        }

    return {}

