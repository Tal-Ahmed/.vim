import platform
import os
import json
import glob
import logging

from collections import OrderedDict

logger = logging.getLogger('ycm_extra_conf_logger')

logger.setLevel(logging.DEBUG)

SOURCE_EXTENSIONS = ['.cc', '.cpp', '.c']
HEADER_EXTENSIONS = ['.h', '.hpp', '.hh']

# Disable generating includes for ats-buildfs
CXX_DISABLE_ATS_BUILDFS_INCLUDES = False

# Blacklist any include that contains the following as a sub dir (does not apply to ats-buildfs includes)
CXX_BLACKLIST_INCLUDE_SUBDIR = ['.git', '.svn', 'example', '.deps', 'doc', 'docs', '.libs', 'build', 'release', 'config', 'ats-tester', 'test', 'perl', 'src/plugins', 'src/tools']

# Which dirs to check for a corresponding source file
CXX_CORRESPONDING_SRC_FILE_DIR = ['/', '/../cpp/']

# Whitelist any include that contains the following as a sub dir
CXX_WHITELIST_INCLUDE_SUBDIR = ['include']

# Whitelist any local include that contains the following as a sub dir
CXX_WHITELIST_LOCAL_INCLUDE_SUBDIR = ['include', 'src', 'cpp']

# Create 1-1 mapping between the following products
# If MP includes one, it must include the other
CXX_ADDITIONAL_LIBRARIES = {'ats-lib-yaml-cpp': ('ATS-lib-li-yamlcpp', [], '*.*.*'), 'ATS-lib-li-yamlcpp': ('ats-lib-yaml-cpp', [], '*.*.*')}


# Manually insert products
CXX_WHITELIST_LIBRARIES = OrderedDict({'ats-lib-atscppapi': ('ats-lib-atscppapi', [], '4.0.18'), 'ats-lib-boost': ('ats-lib-boost', [], '1.41.0.0')})

def GetUserName():
    return os.getlogin()


def IsValidInclude(include):
    if 'ats-buildfs' in include:
        return True
    for bad_dir in CXX_BLACKLIST_INCLUDE_SUBDIR:
        if bad_dir in include:
            return False 
    return True


def GetIncludePrefix(include):
    if 'ats-buildfs' in include:
        return include
    prefix = '-I'
    return prefix + include


# Compilation flags for C/C++ files
flags = [
    '-x',
    'c++',
    '-std=c++11',
    '-g',
    '-pthread',
    '-fPIC',
    '-Werror',
    '-Wno-deprecated',
    '-Wno-expansion-to-defined',
    '-Wno-invalid-offsetof',
    '-D__STDC_FORMAT_MACROS ',
    # You 100% do NOT need -DUSE_CLANG_COMPLETER and/or -DYCM_EXPORT in your flags;
    # only the YCM source code needs it.
    '-DUSE_CLANG_COMPLETER',
    '-DYCM_EXPORT=',
]


def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS


def StandardizeVersionNumber(version):
    return version


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


def GetHighestVersionProduct(librarypath, version):
    if not os.path.exists(librarypath):
        logger.debug('Could not open product %s' % librarypath)
        return None
    version = StandardizeVersionNumber(version)
    logger.debug('Getting highest version product for %s' % librarypath + '/' + version)
    librarypaths = glob.glob(librarypath + '/' + version)
    librarypaths.sort(reverse=True)
    if len(librarypaths) == 0:
        logger.debug('Could not get highest version product for %s' % librarypath + '/' + version)
        return None
    logger.debug('Found highest version product %s' % librarypaths[0])
    return librarypaths[0]


def DirContainsHeaderFile(dirname, files):
    for filename in files:
        if IsHeaderFile(filename):
            return True
    return False


def GenerateLibraryIncludeForAtsBuildFs(productname, libraries, version):
    return []
    logger.debug('Short-circuiting to ats-buildfs-rhel7')
    return ['--no-sysroot-suffix --sysroot=/home/mtalha/native-repo/com.linkedin.ats-buildfs-rhel7/ats-buildfs-rhel7/0.2.8']


def GenerateLibraryIncludeForProduct(productname, libraries, version):
    if len(libraries) == 0:
        libraries.append(productname)
    includes = []
    for library in libraries:
        logger.debug('Generating library includes for %s::%s::%s' % (productname, library, version))
        if 'ats-buildfs' in productname:
            includes.extend(GenerateLibraryIncludeForAtsBuildFs(productname, libraries, version))
            continue
        basename = GetHighestVersionProduct(
            '/home/%s/native-repo/com.linkedin.%s/%s' % (GetUserName(), productname, library), version)
        if basename is None:
            continue
        for root, dirs, files in os.walk(basename):
            for d in CXX_WHITELIST_INCLUDE_SUBDIR:
                if root.endswith(d):
                    includes.append(root)
                    continue
    return includes


def GenerateLibraryIncludes(filename, imported_products):
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/product-spec.json'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return []

    productspec = basename + '/product-spec.json'
    includes = []

    with open(productspec, 'r') as f:
        json_productspec = json.load(f)
        for productname in json_productspec['product']:
            if productname not in imported_products:
                libraries = json_productspec['product'][productname]['libraries']
                version = json_productspec['product'][productname]['version']
                includes.extend(GenerateLibraryIncludeForProduct(productname, libraries, version))
                imported_products[productname] = True
                if productname in CXX_ADDITIONAL_LIBRARIES and CXX_ADDITIONAL_LIBRARIES[productname][0] not in imported_products:
                    includes.extend(GenerateLibraryIncludeForProduct(
                        CXX_ADDITIONAL_LIBRARIES[productname][0],
                        CXX_ADDITIONAL_LIBRARIES[productname][1],
                        CXX_ADDITIONAL_LIBRARIES[productname][2]))
                    imported_products[CXX_ADDITIONAL_LIBRARIES[productname][0]] = True
    return includes


def GenerateWhitelistLibraryIncludes(imported_products):
    includes = []
    for productname in CXX_WHITELIST_LIBRARIES:
        if productname not in imported_products:
            includes.extend(GenerateLibraryIncludeForProduct(
                CXX_WHITELIST_LIBRARIES[productname][0], 
                CXX_WHITELIST_LIBRARIES[productname][1], 
                CXX_WHITELIST_LIBRARIES[productname][2]))
            imported_products[productname] = True
    return includes


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
            if d in root:
                logger.debug('Found local include %s' % root)
                includes.append(root)
                continue
    return includes


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


def GetRemoveDuplicateIncludes(includes):
    imported_includes = {}
    valid_includes = []
    for include in includes:
        if include not in imported_includes:
            valid_includes.append(include)
            imported_includes[include] = True
    return valid_includes


def Settings(**kwargs):
    filename = kwargs['filename']
    language = kwargs['language']

    if not filename.startswith('/home/%s' % GetUserName()):
        logger.debug('Tried to get settings for %s, ignoring' % filename)
        return {}

    if language == 'cfamily':
        filename = FindCorrespondingSourceFile(filename)

        imported_products = {}
        # cxx_flags = ['-I/home/mtalha/native-repo/com.linkedin.ats-buildfs-rhel7/ats-buildfs-rhel7/0.2.8/usr/include']
        cxx_flags = []
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateLocalInclude(filename)])
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateWhitelistLibraryIncludes(imported_products)])
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateLibraryIncludes(filename, imported_products)])

        cxx_flags = GetRemoveBlacklistedIncludes(cxx_flags)
        cxx_flags = GetRemoveDuplicateIncludes(cxx_flags)

        return {
            'flags': flags + cxx_flags,
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

