import platform
import os
import json
import glob
import logging

logger = logging.getLogger('ycm_extra_conf_logger')

logger.setLevel(logging.DEBUG)

SOURCE_EXTENSIONS = ['.cpp', '.cc', '.c']
HEADER_EXTENSIONS = ['.h', '.hh', '.hpp']

# Disable generating includes for ats-buildfs
CXX_DISABLE_ATS_BUILDFS_INCLUDES = False

# Blacklist any include that contains the following as a sub dir (does not apply to ats-buildfs includes)
CXX_BLACKLIST_INCLUDE_SUBDIR = ['.git', 'example', '.deps', 'doc', 'docs', '.libs', 'build', 'release', 'config', 'ats-tester', 'test', 'msinttypes']

# Which dirs to check for a corresponding source file
CXX_CORRESPONDING_SRC_FILE_DIR = ['/../cpp/', '/']

# Whitelist any include that contains the following as a sub dir
CXX_WHITELIST_INCLUDE_SUBDIR = ['include', 'cpp', 'src']

# Whitelist any local include that contains the following as a sub dir
CXX_WHITELIST_LOCAL_INCLUDE_SUBDIR = ['include', 'cpp', 'src']

# Create 1-1 mapping between the following products
# If MP includes one, it must include the other
CXX_ADDITIONAL_LIBRARIES = {'ats-lib-yaml-cpp': ('ATS-lib-li-yamlcpp', [], '*.*.*'), 'ATS-lib-li-yamlcpp': ('ats-lib-yaml-cpp', [], '*.*.*')}

# Manually insert product if product-spec.json doesn't include it
CXX_WHITELIST_LIBRARIES = {'ats-core': ('ats-core', ['ats6'], '*.*.*'), 'ats-buildfs-rhel7': ('ats-buildfs-rhel7', [], '*.*.*')}


def GetUserName():
    return os.getlogin()


def IsValidInclude(include):
    if 'ats-buildfs' in include:
        return True
    for bad_dir in CXX_BLACKLIST_INCLUDE_SUBDIR:
        if bad_dir in include:
            return False 
    return True


def GetLibraryInclude(library, version):
    return '/home/%s/native-repo/%s/%s/%s/include' % (GetUserName(), library, library, version)


def GetIncludePrefix(include):
    prefix = '-I'
    if 'ats-buildfs' in include:
        prefix = '-isystem '
    return prefix + include


# Compilation flags for C/C++ files
flags = [
    '-g',
    '-pthread',
    '-Werror',
    '-Wno-deprecated',
    '-Wno-expansion-to-defined',
    '-fPIC',
    # You 100% do NOT need -DUSE_CLANG_COMPLETER and/or -DYCM_EXPORT in your flags;
    # only the YCM source code needs it.
    '-DUSE_CLANG_COMPLETER',
    '-DYCM_EXPORT=',
    # Set language (C++)
    '-x',
    'c++',
    # C++11
    '-std=c++11',
    '-I' + GetLibraryInclude('boost', '1.55.0.6'),
    '-I/home/mtalha/native-repo/jemalloc/jemalloc/1003.6.1.4/include',
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
                replacement_file = os.path.dirname(filename) + d + basename + extension
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


def GenerateLibraryIncludeForAtsBuildFs(basename):
    logger.debug('Generating library includes for ats-buildfs')
    includes = []
    already_included = {}
    if CXX_DISABLE_ATS_BUILDFS_INCLUDES:
        logger.debug('Disabled, early returning..')
        return []
    for root, dirs, files in os.walk(basename):
        if root not in already_included and DirContainsHeaderFile(root, files):
            logger.debug('Found include dir %s' % root)
            includes.append(root)
            already_included[root] = True
    return includes


def GenerateLibraryIncludeForProduct(productname, libraries, version):
    if len(libraries) == 0:
        libraries.append(productname)
    includes = []
    for library in libraries:
        logger.debug('Generating library includes for %s::%s::%s' % (productname, library, version))
        basename = GetHighestVersionProduct(
            '/home/%s/native-repo/com.linkedin.%s/%s' % (GetUserName(), productname, library), version)
        if basename is None:
            continue
        if 'ats-buildfs' in basename:
            includes.extend(GenerateLibraryIncludeForAtsBuildFs(basename))
            continue
        for root, dirs, files in os.walk(basename):
            for d in CXX_WHITELIST_INCLUDE_SUBDIR:
                if d in root and root != basename:
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
            libraries = json_productspec['product'][productname]['libraries']
            version = json_productspec['product'][productname]['version']
            imported_products[productname] = True
            if productname in CXX_ADDITIONAL_LIBRARIES:
                includes.extend(GenerateLibraryIncludeForProduct(
                    CXX_ADDITIONAL_LIBRARIES[productname][0], 
                    CXX_ADDITIONAL_LIBRARIES[productname][1], 
                    CXX_ADDITIONAL_LIBRARIES[productname][2]))
            includes.extend(GenerateLibraryIncludeForProduct(productname, libraries, version))

    return includes


def GenerateWhitelistLibraryIncludes(imported_products):
    # Hacky way to avoid importing ats-buildfs-rhel7 as well
    if 'ats-buildfs-rhel6' in imported_products:
        imported_products['ats-buildfs-rhel7'] = True

    includes = []
    for productname in CXX_WHITELIST_LIBRARIES:
        if productname not in imported_products:
            includes.extend(GenerateLibraryIncludeForProduct(
                CXX_WHITELIST_LIBRARIES[productname][0], 
                CXX_WHITELIST_LIBRARIES[productname][1], 
                CXX_WHITELIST_LIBRARIES[productname][2]))

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


def Settings(**kwargs):
    filename = kwargs['filename']
    language = kwargs['language']

    if not filename.startswith('/home/%s' % GetUserName()):
        logger.debug('Tried to get settings for %s, ignoring' % filename)
        return {}

    if language == 'cfamily':
        filename = FindCorrespondingSourceFile(filename)

        imported_products = {}
        cxx_flags = []
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateLocalInclude(filename)])
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateWhitelistLibraryIncludes(imported_products)])
        cxx_flags.extend([GetIncludePrefix(include) for include in GenerateLibraryIncludes(filename, imported_products)])

        cxx_flags = GetRemoveBlacklistedIncludes(cxx_flags)

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

