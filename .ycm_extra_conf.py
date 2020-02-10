import os
import subprocess
import logging

from collections import OrderedDict

logger = logging.getLogger('ycm_extra_conf_logger')

logger.setLevel(logging.DEBUG)

SOURCE_EXTENSIONS = ['.cc', '.cpp', '.c']
HEADER_EXTENSIONS = ['.h', '.hpp', '.hh']

# Whether or not to print cmd
DEBUG_CMD = False

# Whether or not to disable local includes
DISABLE_LOCAL_INCLUDES = False

# Which dirs to check for a corresponding source file
CXX_CORRESPONDING_SRC_FILE_DIR = ['/', '/../cpp/']

# Whitelist any local include that contains the following as a sub dir
CXX_WHITELIST_LOCAL_INCLUDE_SUBDIR = ['include', 'src', 'cpp']

# Blacklist any include that contains the following as a sub dir (does not apply to ats-buildfs includes)
CXX_BLACKLIST_INCLUDE_SUBDIR = ['.git', '.svn', 'python', 'example', '.deps', 'doc', 'docs', '.libs', 'build', 'release', 'config', 'ats-tester', 'test', 'perl']


def GetUserName():
    return os.getlogin()


def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS


def IsValidInclude(include):
    for bad_dir in CXX_BLACKLIST_INCLUDE_SUBDIR:
        if bad_dir.lower() in include:
            return False
    return True


def GetRemoveBlacklistedIncludes(includes):
    logger.debug('Generating valid includes')
    valid_includes = []
    for include in includes:
        if IsValidInclude(include):
            logger.debug('Found valid include %s' % include)
            valid_includes.append(include)
        else:
            logger.debug('Found invalid include %s' % include)
    return valid_includes


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


def GenerateLocalInclude(filename):
    logger.debug('Generating local includes for %s' % filename)
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build.gradle'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return []
    includes = []
    for root, dirs, files in os.walk(basename):
        for d in CXX_WHITELIST_LOCAL_INCLUDE_SUBDIR:
            if d in root and 'build' not in root:
                logger.debug('Found local include %s' % root)
                includes.append(root)
                continue
    return includes


def GetAtsBuildFsSpecifies():
    return [
        '-I/home/%s/native-repo/com.linkedin.ats-buildfs-rhel7/ats-buildfs-rhel7/0.2.8/usr/include' % GetUserName(),
        '-I/home/%s/native-repo/com.linkedin.ats-buildfs-rhel7/ats-buildfs-rhel7/0.2.8/usr/include/c++/4.8.2/x86_64-redhat-linux/include' % GetUserName(),
        '-I/home/%s/native-repo/com.linkedin.ats-buildfs-rhel7/ats-buildfs-rhel7/0.2.8/usr/include/c++/4.8.2/x86_64-redhat-linux' % GetUserName(),
    ]


def Settings(**kwargs):
    filename = kwargs['filename']
    language = kwargs['language']

    if not filename.startswith('/home/%s' % GetUserName()):
        logger.debug('Tried to get settings for %s, ignoring' % filename)
        return {}

    if language == 'cfamily':
        if not filename.startswith('/home/%s/dev/ats-plugins' % GetUserName()) and \
                not filename.startswith('/home/%s/dev/ats-libs' % GetUserName()):
            logger.debug('Auto complete only enabled for ats-plugins and ats-libs')
            return {}

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
            'echo " %s"' % " ".join(GetAtsBuildFsSpecifies())
        ]

        if DEBUG_CMD:
            logger.debug('Excuting cmd:')
            logger.debug(';'.join(cmds))

        cmd_out_stream = subprocess.Popen(';'.join(cmds), shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_out = cmd_out_stream.stdout.read()
        cmd_out_stderr = cmd_out_stream.stderr.read()

        if len(cmd_out_stderr) != 0:
            logger.debug('Cmd returned error')
            logger.debug(cmd_out_stderr)
            return {}

        logger.debug('Cmd returned:')
        logger.debug(cmd_out)

        cxx_flags = ['-x', 'c++', '-g', '-DUSE_CLANG_COMPLETER', '-DYCM_EXPORT=']
        cxx_flags.extend(str(cmd_out).strip().split(' ')[3:])
        if not DISABLE_LOCAL_INCLUDES:
            cxx_flags.extend(GetRemoveBlacklistedIncludes(['-I' + include for include in GenerateLocalInclude(filename)]))

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

