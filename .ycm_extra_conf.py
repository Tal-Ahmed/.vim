import platform
import os
import json
import glob

SOURCE_EXTENSIONS = ['.cpp', '.cc', '.c']
HEADER_EXTENSIONS = ['.h', '.hpp']
CXX_BLACKLIST_LIBRARIES = ['ats-tester', 'ats-buildfs-rhel7', 'ats-buildfs-rhel6']
CXX_WHITELIST_LIBRARIES = [('ats-core', ['ats6'], '*.*.*')]
CXX_ADDITIONAL_LIBRARIES = {'ats-lib-yaml-cpp': ('ATS-lib-li-yamlcpp', [], '*.*.*')}
PY_LIBRARIES = [('ats-tester', '*.*.*')]


def GetUserName():
    return os.getlogin()


def GetLibraryInclude(library, version):
    os.path.dirname
    return '/home/%s/native-repo/%s/%s/%s/include' % (GetUserName(), library, library, version)


# Compilation flags for C/C++ files
flags = [
    '-g',
    '-pthread',
    '-Werror',
    '-Wno-deprecated',
    '-fPIC',
    # You 100% do NOT need -DUSE_CLANG_COMPLETER and/or -DYCM_EXPORT in your flags;
    # only the YCM source code needs it.
    '-DUSE_CLANG_COMPLETER',
    '-DYCM_EXPORT=',
    # Set language (C++)
    '-x',
    'c++',
    # Set library includes
    '-I',
    GetLibraryInclude('boost', '1.55.0.6'),
    '-I',
    GetLibraryInclude('ats-lib-boost', '1.41.0.0'),
    # C++11
    '-std=c++11',
]


def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS


def FindCorrespondingSourceFile(filename):
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for extension in SOURCE_EXTENSIONS:
            replacement_file = os.path.dirname(filename) + '/../cpp/' + basename + extension
            if os.path.exists(replacement_file):
                return replacement_file
    return filename


def GetHighestVersionLibrary(librarypath, version):
    if not os.path.exists(librarypath):
        return None
    librarypaths = glob.glob(librarypath + '/' + version)
    librarypaths.sort(reverse=True)
    if len(librarypaths) == 0:
        print("Could not resolve: " + librarypath + '/' + version)
        return None
    return librarypaths[0] + '/include'


def GenerateLibraryIncludes(filename):
    if not filename.startswith('/home/%s' % GetUserName()):
        return []
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/product-spec.json'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return []
    productspec = basename + '/product-spec.json'
    includes = []
    additional = []
    with open(productspec, 'r') as f:
        json_productspec = json.load(f)
        for productname in json_productspec['product']:
            if productname in CXX_BLACKLIST_LIBRARIES:
                continue
            if productname in CXX_ADDITIONAL_LIBRARIES:
                additional.append(CXX_ADDITIONAL_LIBRARIES[productname])
            libraries = json_productspec['product'][productname]['libraries']
            if productname != 'ats-core':
                libraries.append(productname)
            version = json_productspec['product'][productname]['version']
            for library in libraries:
                libraryinclude = GetHighestVersionLibrary(
                        '/home/%s/native-repo/com.linkedin.%s/%s' % (GetUserName(), productname, library), version)
                if libraryinclude is None:
                    continue
                includes.append(libraryinclude)
    includes.extend(GenerateAdditionalLibraryIncludes(additional))
    return includes


def GenerateAdditionalLibraryIncludes(additional):
    includes = []
    for (product, libraries, version) in additional:
        if len(libraries) == 0:
            libraryinclude = GetHighestVersionLibrary(
                    '/home/%s/native-repo/com.linkedin.%s/%s' % (GetUserName(), product, product), version)
            if libraryinclude is not None:
                includes.append(libraryinclude)
        else:
            for library in libraries:
                libraryinclude = GetHighestVersionLibrary(
                        '/home/%s/native-repo/com.linkedin.%s/%s' % (GetUserName(), product, library), version)
                if libraryinclude is not None:
                    includes.append(libraryinclude)
    return includes


def GenerateLocalInclude(filename):
    if not filename.startswith('/home/%s' % GetUserName()):
        return []
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build.gradle'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return []
    includes = []
    for root, dirs, files in os.walk(basename):
        if 'release' in root or 'build' in root or 'config' in root:
            continue
        if 'include' in root or 'cpp' in root or 'src' in root:
            includes.append(root)
    return includes


def GetPythonInterpreterPath(filename):
    if not filename.startswith('/home/%s' % GetUserName()):
        return ''
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return ''
    venvpath = basename + '/build/functional_test/venv/bin/python'
    if not os.path.exists(venvpath):
        return ''
    return venvpath


def GetPythonSitePackages(filename):
    if not filename.startswith('/home/%s' % GetUserName()):
        return ''
    basename = os.path.dirname(filename)
    while basename != '/home/%s' % GetUserName() and not os.path.exists(basename + '/build'):
        basename = os.path.dirname(basename)
    if basename == '/home/%s' % GetUserName():
        return ''
    sitepackages = basename + '/build/functional_test/venv/lib/python3.7/site-packages'
    if not os.path.exists(sitepackages):
        return ''
    return sitepackages


def Settings(**kwargs):
    if kwargs['language'] == 'cfamily':
        filename = FindCorrespondingSourceFile(kwargs['filename'])
        cxx_flags = flags + ['-I' + include for include in GenerateLocalInclude(filename) + GenerateLibraryIncludes(filename) + GenerateAdditionalLibraryIncludes(CXX_WHITELIST_LIBRARIES)]
        return {
            'flags': cxx_flags,
            'override_filename': filename
        }
    elif kwargs['language'] == 'python':
        return {
            'interpreter_path': GetPythonInterpreterPath(kwargs['filename']),
            'sys_path': [
                GetPythonSitePackages(kwargs['filename'])
            ]
        }
    return {}

