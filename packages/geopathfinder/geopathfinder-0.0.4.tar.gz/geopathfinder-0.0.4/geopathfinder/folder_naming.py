# Copyright (c) 2018, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Module handling folder trees.
"""

import os
import glob
import copy
import shutil
import warnings

from datetime import datetime

import regex as re
import numpy as np
import pandas as pd


class SmartPath(object):

    """
    Base class for the single path structure to a data set.
    - allows building a path,
    - searching files with temporal slicing,
    - creating a pandas.DataFrame from a folder
    """

    def __init__(self, levels, hierarchy, make_dir=False):
        """

        Parameters
        ----------
        levels : dict
            dictionary assigning the name of levels to the hierarchy
        hierarchy : list of str
            List defining the order of the levels
        make_dir : bool, optional
            if set to True, then the full path of
            the SmartPath is created in the filesystem (default: False).
        """

        if all([x in hierarchy for x in list(levels.keys())]):

            self.levels = levels
            self.hierarchy = hierarchy

            directory = self.build_levels()
            self.directory = directory

            self.file_count = 0
            self.file_register = []

            if make_dir:
                self.make_dir()

        else:
            raise ValueError('Levels are not reflected by the given hierarchy!')

    def __getitem__(self, level):
        """
        Short link for path, down to 'level'.
        Usage: path2level = your_smart_path[level]

        Parameters
        ----------
        level : str
            Name of level in hierarchy

        Returns
        -------
        path : str
            Path from root to level.
        """
        return self.get_level(level)


    def print_file_register(self):
        '''
        Nice function to print nicely all registered files to screen.
        '''

        print('\n'.join(self.file_register))


    def print_dir(self):
        '''
        Nice function to print nicely the directory of the path.
        '''

        print(self.directory)


    def get_dir(self, make_dir=False):
        """
        Get directory.

        Parameters
        ----------
        make_dir : bool, optional
            Create directory if not exists (default: False).

        Returns
        -------
        folder : str
            Full path of the SmartPath
        """
        if make_dir:
            self.make_dir()

        return self.directory

    def make_dir(self):
        """
        Creates directory from root to deepest level
        """
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def build_levels(self, level='', make_dir=False):
        """

        Parameters
        ----------
        level : str, optional
            Name of level in hierarchy
        make_dir : bool, optional
            creates the directory until level

        Returns
        -------
        path : str
            Full path of the SmartPath (to the deepest level)
        """
        directory = r''

        for h in self.hierarchy:
            if self.levels[h] is None:
                break
            else:
                directory = os.path.join(directory, self.levels[h])
                if h == level:
                    break

        if make_dir:
            if not os.path.exists(directory):
                os.makedirs(directory)

        return directory

    def get_level(self, level):
        """
        Gets the path to the level.

        Parameters
        ----------
        level : str
            Name of level in hierarchy.

        Returns
        -------
        path : str
            Path from root to level.
        """
        if level in self.hierarchy:
            return self.build_levels(level=level)
        else:
            print('\'{}\' is not part of the path\'s hierarchy. '
                  'Try on of {}.'.format(level, self.hierarchy))


    def remove_level(self, level):
        '''
        In the SmartPath-instance, it removes a level from the hierarchy
        and level dictionary.

        Parameters
        ----------
        level : str
            Name of level in hierarchy.
        '''

        if level in self.hierarchy:

            self.levels.pop(level)
            self.hierarchy.remove(level)

            self.__init__(self.levels, self.hierarchy)

        else:
            print('Level \'{}\' is not in hierarchy!')


    def cutoff_level(self, level):
        '''
        Removes all levels that are higher or equal to given level.

        Parameters
        ----------
        level : str
            String of the level that should be removed, together will all
            higher levels.
        '''
        if level in self.hierarchy:

            for h in copy.copy(self.hierarchy):
                if h != level:
                    self.remove_level(h)
                else:
                    self.remove_level(h)
                    break

        else:
            print('Level \'{}\' is not in hierarchy!')


    def base_onto_root(self, root):
        '''
        Adds as first level 'root' to the SmartPath-instance.

        Parameters
        ----------
        root : str
            String of the root directory
        '''

        if 'root' in self.hierarchy:
            self.remove_level('root')

        self.levels.update({'root': root})
        self.hierarchy = ['root'] + self.hierarchy

        self.__init__(self.levels, self.hierarchy)


    def expand_full_path(self, level, files):
        """
        Joins the path at level with given filenames.

        Parameters
        ----------
        level : str
            Name of level in hierarchy.
        files : list of str
            List of file names.

        Returns
        -------
        path : str
            Full file path.
        """
        return expand_full_path(self[level], files)


    def search_files(self, level, pattern='', full_paths=False):
        """
        Searches files meeting the regex pattern at level in the SmartPath

        Parameters
        ----------
        level : str
            Name of level in hierarchy
        pattern : str tuple, optional
            strings defining search pattern for file search
            e.g. ('C1003', 'E048N012T6')
        full_paths : bool, optional
            If True, full paths will be included in dataframe (default: False)

        Returns
        -------
        filenames : list of str
            File names at the level.
        """
        if level not in self.levels.keys():
            return []
        else:
            return regex_file_search(self.build_levels(level), pattern,
                                 full_paths=full_paths)[0]


    def search_files_ts(self, level, pattern='',
                        date_position=1, date_format='%Y%m%d_%H%M%S',
                        starttime=None, endtime=None, full_paths=False):
        """
        Function searching files at a level in the SmartPath,
        returning the filenames and the datetimes as pd.DataFrame

        Parameters
        ----------
        level : str
            name of level in hierarchy
        pattern : str tuple, optional
            strings defining search pattern for file search
            e.g. ('C1003', 'E048N012T6')
        date_position : int
            position of first character of date string in name of files
        date_format : str
            string with the datetime format in the filenames.
            e.g. '%Y%m%d_%H%M%S' reflects '20161224_000000'
        starttime : str or datetime, optional
            earliest date and time, if str must follow "date_format"
        endtime : str or datetime, optional
            latest date and time, if str must follow "date_format"
        full_paths : bool, optional
            should full paths be in the dataframe? default: False

        Returns
        -------
        df : pandas.DataFrame
            Dataframe holding the filenames and the datetimes
        """

        files = self.search_files(level, pattern=pattern)
        times = extract_times(
            files, date_position=date_position, date_format=date_format)

        if full_paths:
            files = self.expand_full_path(level, files)

        df = pd.DataFrame({'Files': files}, index=times)
        df.sort_index(inplace=True)

        if (starttime is not None) or (endtime is not None):
            if not isinstance(starttime, datetime):
                starttime = datetime.strptime(starttime, date_format)
            if not isinstance(endtime, datetime):
                endtime = datetime.strptime(endtime, date_format)
            df = df[starttime:endtime]

        return df


    def build_file_register(self, level=None, pattern='.'):
        """
        Builds a file register collecting files at all levels in the SmartPath.

        Parameters
        ----------
        level : str, optional
            deepest level that should be included in the file register
        pattern : str tuple, optional
            strings defining search pattern for file search
            e.g. ('C1003', 'E048N012T6')
        """
        file_register = []
        file_count = 0
        if level is None:
            idx = self.hierarchy
        else:
            idx = self.hierarchy[0:self.hierarchy.index(level) + 1]
        for h in idx:
            if self.levels[h] is not None:
                r, c = regex_file_search(
                    self.build_levels(level=h),
                    pattern, full_paths=True)
                file_register += r
                file_count += c

        self.file_register = file_register
        self.file_count = file_count


class NullSmartPath(SmartPath):
    '''
    Class for non-exiting paths. Helps to avoid errors.
    '''
    def __init__(self):
        super(NullSmartPath, self).__init__({}, [], make_dir=False)


class SmartTree(object):
    '''
    Class for collecting multiple SmartPaths() at one root path.
    '''

    def __init__(self, root, hierarchy, make_dir=False):
        '''
        Initialises a SmartTree object for a given rootdirectory and hierarchy.

        Parameters
        ----------
        root : str
            directory path to root of directory tree.
        hierarchy : list of str
            List defining the order of the levels
        make_dir : bool, optional
            creates the root directory
        '''

        if not os.path.exists(root) and make_dir == False:
            raise OSError('Given directory for attribute \'root\', '
                          '\'{}\', does not exist!'.format(root))

        self.root = root
        self.dirs = {}
        self.hierarchy = hierarchy
        self.dir_count = 0
        self.file_count = 0
        self.file_register = []

        if make_dir:
            if not os.path.exists(self.root):
                os.makedirs(self.root)


    def __getitem__(self, pattern):
        '''
        Shortcut for get_smartpath()

        Usage-example: smarttree['C1003', 'E048N012T6']
        '''

        return self.get_smartpath(pattern)


    def print_all_dirs(self):
        '''
        Nice function to print nicely all directories to screen.
        I'm proud of this function!
        '''

        print('\n'.join(self.get_all_dirs()))


    def print_file_register(self):
        '''
        Nice function to print nicely all registered files to screen.
        '''

        print('\n'.join(self.file_register))


    def print_collect_level(self, level, pattern=None, unique=False):
        '''
        Nice function to print nicely output from collect_level()
        '''

        print('\n'.join(self.collect_level(level, pattern=pattern,
                                           unique=unique)))


    def print_collect_level_topnames(self, level, pattern=None, unique=True):
        '''
        Nice function to print nicely output from collect_level_topnames()
        '''

        print('\n'.join(self.collect_level_topnames(level, pattern=pattern,
                                                    unique=unique)))


    def file_register_search(self, pattern, full_paths=True):
        """
        Searches files in register meeting the regex pattern

        Parameters
        ----------
        pattern : str tuple, optional
            strings defining search pattern for file search
            e.g. ('C1003', 'E048N012T6')
        full_paths : bool, optional
            If True, full paths will be included in dataframe (default: False)
        Returns
        -------
        filenames : str or list of str
            File names

        """
        pattern = patterns_2_regex(pattern)

        regex = re.compile(pattern)
        files = [f for f in self.file_register if regex.match(os.path.basename(f))]

        if not full_paths:
            files = [os.path.basename(f) for f in files]

        if len(files) == 1:
            file = files[0]
            return file
        else:
            return sorted(files)


    def get_all_smartpaths(self):
        '''
        Returns SmartPaths in the SmartTree

        Returns
        -------
        list of SmartPaths
            List of all included SmartPaths
        '''

        return list(self.dirs.values())


    def get_all_dirs(self):
        '''
        Returns all full paths in the SmartTree

        Returns
        -------
        list
            Sorted list of all full paths
        '''

        return sorted(list(self.dirs.keys()))


    def count_dirs(self):
        '''
        Sets the dir_count the SmartTree
        '''

        self.dir_count = len(self.dirs)


    def get_smartpath(self, pattern):
        '''
        Returns one SmartPath-object from the SmartTree that matches with
        the pattern. If more than one match, None is returned.

        Parameters
        ----------
        pattern : str tuple
            strings defining search pattern for path search
            e.g. ('C1003', 'E048N012T6')

        Returns
        -------
        SmartPath
            The path object matching the pattern.
        '''

        pattern = patterns_2_regex(pattern)

        paths = self.dirs.keys()

        matching_paths = []

        regex = re.compile(pattern)
        matching_paths += [m for m in paths if regex.match(m)]

        if len(matching_paths) == 0:
            warnings.warn('get_smartpath(): No matches for "pattern"!')
            return NullSmartPath()
        elif len(matching_paths) > 1:
            warnings.warn('get_smartpath(): Multiple matches for "pattern"!')
            return NullSmartPath()
        else:
            return self.dirs[matching_paths[0]]


    def collect_level(self, level, pattern=None, unique=False):
        '''
        Returns a list of paths at given level.

        Parameters
        ----------
        level : str
            name of level in hierarchy
        pattern : str tuple, optional
            strings defining search pattern for path search
            e.g. ('C1003', 'E048N012T6')
        unique : bool, optional
            if set, a list of unique paths is returned
        Returns
        -------
        list of str
            list of paths at given level, matching the given pattern
        '''

        result = []

        for _, smartpath in self.dirs.items():
            if smartpath.levels[level] is not None:

                if pattern is not None:
                    rpattern = patterns_2_regex(pattern)
                    regex = re.compile(rpattern)
                    if regex.match(smartpath.levels[level]):
                        result.append(smartpath[level])
                else:
                    result.append(smartpath[level])

        if unique:
            result = list(set(result))

        return sorted(result)


    def collect_level_topnames(self, level, pattern=None, unique=True):
        '''
        Returns list of topnames of folders at given level.

        Parameters
        ----------
        level : str
            name of level in hierarchy
        pattern : str tuple, optional
            strings defining search pattern for path search
            e.g. ('C1003', 'E048N012T6')
        unique : bool, optional
            if set, a list of unique paths is returned

        Returns
        -------
        topnames : list of str
            list of folder-topnames at given level, matching the given pattern
        '''

        paths = self.collect_level(level, pattern=pattern, unique=unique)

        topnames = [x.split(os.sep)[-1] for x in paths]

        return topnames


    def add_smartpath(self, smartpath, make_dir=False):
        '''
        Adds a SmartPath-object to the SmartTree.

        Parameters
        ----------
        smartpath : SmartPath
            A SmartPath object. Only valid if hierarchy is compatible with the
            hierarchy of the SmartTree.
        make_dir : bool, optional
            creates the full directory of the SmartPath
        '''

        if isinstance(smartpath, SmartPath):

            smartpath.base_onto_root(self.root)

            if self.hierarchy == smartpath.hierarchy:

                self.dirs.update({smartpath.get_dir(): smartpath})
                self.count_dirs()

            else:
                print("SmartPath is not compatible with SmartTree: "
                      "Hierarchies do not correspond!")

            if make_dir:
                smartpath.make_dir()


    def remove_smartpath(self, key):
        '''
        Removes the SmartPath with 'key' from the SmartTree

        Parameters
        ----------
        key : str
            Path representing the key for the SmartPath
        '''

        self.dirs.pop(key)
        self.count_dirs()


    def trim2branch(self, level, pattern, register_file_pattern=None):
        '''
        Returns a branch (a subtree) of a SmartTree that matches with
        the pattern at the given level.

        Parameters
        ----------
        level : str
            Name of level in hierarchy.
            e.g. 'wflow'
        pattern : str
            string defining search pattern at given level
            e.g. 'C1003'

        Returns
        -------
        branch : SmartTree
            SmartTree object that describes the seeked branch,
            part of current SmartTree
        '''

        branch = copy.deepcopy(self)

        branch_path = self.collect_level(level, pattern=pattern, unique=True)

        if len(branch_path) == 0:
            warnings.warn('trim2branch(): No matches for "pattern" at "level"!')
            return NullSmartTree(self.root)
        elif len(branch_path) > 1:
            warnings.warn('trim2branch(): Multiple matches for "pattern" at "level"!')
            return NullSmartTree(self.root)
        else:
            for d in self.dirs.keys():
                if not branch_path[0] in d:
                    branch.remove_smartpath(d)
                else:
                    branch.dirs.get(d).cutoff_level(level)
                    branch.dirs.get(d).base_onto_root(branch_path[0])

            # update dir_count
            branch.count_dirs()
            # update tree root
            branch.root = branch_path[0]
            # update tree hierarchy
            for h in copy.copy(branch.hierarchy):
                if h != level:
                    branch.hierarchy.remove(h)
                else:
                    branch.hierarchy.remove(h)
                    break
            branch.hierarchy = ['root'] + branch.hierarchy

            file_register = []
            file_count = 0
            # update file_register
            if register_file_pattern is not None:
                for sp in branch.dirs.values():
                    sp.build_file_register(pattern=register_file_pattern)
                    file_register += sp.file_register
                    file_count += sp.file_count

            branch.file_register = file_register
            branch.file_count = file_count

            return branch


    def make_dirs(self):
        '''
        Creates a full path for each of the contained SmartPaths.
        '''

        for _, smartpath in self.dirs.items():
            smartpath.make_dir()


    def copy_smarttree_on_fs(self, target_dir, level=None, level_pattern='',
                             file_pattern=None):
        """
        Copies all files and directories in the SmartTree to a target
        directory, using shutil.copytree().

        Parameters
        ----------
        target_dir : str
            the target directory
        level : str, optional
            if set, only the branch at given "level" and matching given
            "pattern" will be copied. e.g. 'wflow'.
            Otherwise all below root directory will be copied.
        level_pattern : str
            string defining search pattern at given level
            e.g. 'A0202'
        file_pattern : str or tuple of str, optional
            string patterns for file matching.
            when starting with "-" it is interpreted as negative pattern
            that should be excluded from the matches


        Returns
        -------

        """

        if level is None:
            source_dir = self.root
            base_folder = self.collect_level_topnames('root')[0]
        else:
            branch = self.trim2branch(level, level_pattern, register_file_pattern=file_pattern)
            source_dir = branch.collect_level('root', level_pattern, unique=True)[0]
            base_folder = branch.collect_level_topnames('root')[0]

        target_dir = os.path.join(target_dir, base_folder)

        copy_tree(source_dir, target_dir, file_pattern=file_pattern)


class NullSmartTree(SmartTree):
    '''
    Class for non-exiting paths. Helps to avoid errors.
    '''
    def __init__(self, root):
        super(NullSmartTree, self).__init__(root, [], make_dir=False)


def create_smartpath(root, hierarchy, levels, make_dir=False):
    '''
    Function for creating a SmartPath().

    Parameters
    ----------
    root : str
        root path of the SmartPath. Gets added as level 'root' in hierarchy.
    hierarchy : list of str
        list defining the order of the levels
    levels : list
        list of the names of levels in the hierarchy
    make_dir : bool, optional
        if set to True, then the full path of
        the SmartPath is created in the filesystem (default: False).

    Returns
    -------
    SmartPath

    '''

    hierarchy = ['root'] + hierarchy
    levels = [root] + levels

    # defining the levels in the directory
    xlevels = {}
    for p in range(len(hierarchy)):
        xlevels.update({hierarchy[p]: levels[p]})

    return SmartPath(xlevels, hierarchy, make_dir=make_dir)


def build_smarttree(root,
                    hierarchy,
                    target_level=None,
                    register_file_pattern=None,
                    trim_level=None,
                    trim_pattern=None):
    '''
    Function walking through directories in root path for building a structure
    of SmartPaths. Can also search for files.
    Attention: The SmartTree is only working properly if all folders in "root"
    follow the "hierarchy"!

    Parameters
    ----------
    root : str
        root path of the SmartTree. Gets added as level 'root' in hierarchy.
    hierarchy : list of str
        List defining the order of the levels
    target_level : str, optional
        Can speed up things: Level name of target tree-depth.
        The SmartTree is only built from directories reaching this level,
        and only built down to this level. If not set, all directories are
        built down to deepest depth.
    register_file_pattern : str tuple, optional
        strings defining search pattern for file search for file_register
        e.g. ('C1003', 'E048N012T6')
        No asterisk is needed ('*')!
        Sequence of strings in given tuple is crucial!
        Be careful: If the tree is large, this can take a while!
    trim_level : str
        Name of level in hierarchy that is subject to the trimming
        e.g. 'grid'
    trim_pattern : str or list of str
        string defining search pattern at trimming level, meaning only paths
        matching this pattern at "trim_level" will be included in the
        SmartTree()
        e.g. 'EQUI7_EU500M'

    Returns
    -------

    '''

    # initialises the SmartTree
    smart_tree = SmartTree(root, ['root'] + hierarchy, make_dir=False)

    # path depth of root
    root_depth = len(root.split(os.sep))

    alldirs = []
    depth = []

    # walk thru the dirs below of root
    for dirpath, dirs, files in os.walk(root, topdown=False):
        alldirs += [dirpath.replace(root, '')]
        depth += [len(dirpath.split(os.sep)) - root_depth]
        # if set, then files are registered
        # (they are in the memory anyway at this moment)
        if trim_level is None:
            if register_file_pattern is not None:
                files, count = regex_file_search(dirpath,
                                                 register_file_pattern,
                                                 full_paths=True)
                smart_tree.file_register += files
                smart_tree.file_count += count
    alldirs = np.array(alldirs)

    # only select paths reaching given target level
    if target_level is not None:
        target_depth = smart_tree.hierarchy.index(target_level)
        singular_paths = alldirs[np.array(depth) == target_depth]

        # reset file register (to register only files down to target level)
        file_register = []

    # select all singular paths that have no children - and drop their parents
    else:
        target_depth = max(depth)
        singular_paths = alldirs[np.array(depth) == target_depth]
        for d in sorted((set(depth)), reverse=True):
            if d == target_depth:
                continue
            paths_at_depth = alldirs[np.array(depth) == d]
            paths_ending = []
            for pad in paths_at_depth:
                if all([pad not in x for x in singular_paths]):
                    paths_ending += [pad]

            singular_paths = np.append(singular_paths, paths_ending)

    # create and append a SmartPath for each singular path
    for fp in singular_paths:
        levels = {}
        sub_levels = fp.split(os.sep)[1:]
        tail_depth = len(sub_levels)
        for p in range(len(hierarchy)):
            if p < tail_depth:
                levels.update({hierarchy[p]: sub_levels[p]})
            else:
                # note sure about this. Potentially causes problems somewhere
                levels.update({hierarchy[p]: None})

        smart_path = SmartPath(levels, hierarchy)

        smart_tree.add_smartpath(smart_path)

        # to register only files down to target level
        if trim_level is None:
            if register_file_pattern is not None and target_level is not None:
                smart_path.build_file_register(level=target_level,
                                               pattern=register_file_pattern)
                file_register += smart_path.file_register

        smart_path = None
        levels = None

    # update self.dir_count
    smart_tree.count_dirs()

    # register only files in paths down to target level
    if trim_level is None:
        if register_file_pattern is not None and target_level is not None:
            smart_tree.file_register = list(set(file_register))
            smart_tree.file_count = len(smart_tree.file_register)

    if trim_level is not None and trim_pattern is not None:
        smart_tree = smart_tree.trim2branch(trim_level, pattern=trim_pattern,
                                            register_file_pattern=register_file_pattern)

    return smart_tree


def expand_full_path(path, files):
    """
    Joins the path at level with given filenames.

    Parameters
    ----------
    level : str
        Name of level in hierarchy.
    files : list of str
        List of file names.

    Returns
    -------
    path : str
        Full file path.
    """
    return [os.path.join(path, f) for f in files]


def reduce_2_basename(files):
    """
    Converts full file paths to file base names.

    Parameters
    ----------
    files : list of str
        list of filepaths

    Returns
    -------
    filenames : list of str
        List of base file names.
    """
    return [os.path.basename(f) for f in files]


def extract_times(files, date_position=1, date_format='%Y%m%d_%H%M%S'):
    """
    Extracts the datetimes from filenames.

    Parameters
    ----------
    files : list of str
        list of strings with filenames or filepaths
    date_position : int
        position of first character of date string in name of files
    date_format: str
        string with the datetime format in the filenames.
        '%Y%m%d_%H%M%S' reflects eg. '20161224_000000'

    Returns
    -------
    times : list of datetime
        List of datetime objects extracted from the filenames.
    """
    if any([os.path.isdir(x) for x in files]):
        files = reduce_2_basename(files)

    times = []
    for f in files:
        t = datetime.strptime(
            f[date_position:date_position + len(date_format) + 2],
            date_format)
        times.append(t)

    return times


def patterns_2_regex(patterns):
    '''
    Converts any string, or tuple of strings, to a regex pattern.

    Parameters
    ----------
    patterns : str or tuple of str
        string patterns for matching.
        when starting with "-" it is interpreted as negative pattern
        that should be excluded from the matches

    Returns
    -------
    str: regex string
    '''

    if isinstance(patterns, str):
        patterns = [patterns]

    regex = [''] * len(patterns)

    for n, p in enumerate(patterns):

        # negative pattern (leads to exclusion)
        if p.startswith('-'):
            regex[n] = '((?!{}).)*$'.format(p[1:])

        # positive pattern (leads to inclusion)
        else:
            regex[n] = '.*{}'.format(p)

    return ''.join(regex)


def regex_file_search(path, pattern, full_paths=True):
    '''
    Carries out the file search using the strings in pattern as regex strings.

    Parameters
    ----------
    path : search in this directory. Subdirectories are ignored.
    pattern : str or tuple of str
        string patterns for matching.
        when starting with "-" it is interpreted as negative pattern
        that should be excluded from the matches
    full_paths : bool, optional
        should full paths be returned? default: True

    Returns
    -------
    tuple
        a tuple (files, count) that contains the file list and the
        count of files

    '''

    pattern = patterns_2_regex(pattern)

    paths = glob.glob(os.path.join(path, '*.*'))
    basenames = reduce_2_basename(paths)

    regex = re.compile(pattern)
    files = [f for f in basenames if regex.match(f)]

    if full_paths:
        files = expand_full_path(path, files)

    return sorted(files), len(files)


def copy_tree(source, dest, file_pattern=None, overwrite=False):
    """
    Copies a directory tree structure.

    Parameters
    ----------
    source : str
        directory that should be copied, recursively
    dest : str
        where the tree should be copied to
    file_pattern : str or tuple of str, optional
        string patterns for file matching.
        when starting with "-" it is interpreted as negative pattern
        that should be excluded from the matches
    overwrite : bool, optional
        should existing files be overwritten? default: False

    """

    # only files matching regex pattern are copied
    if file_pattern is not None:
        fpattern = patterns_2_regex(file_pattern)
        regex = re.compile(fpattern)

    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)

        # all files found
        for file in files:

            if file_pattern is not None:
                include = regex.match(file)
            else:
                include = True

            # proceed if match is given or not required
            if include:
                rel_path = root.replace(source, '').lstrip(os.sep)
                dest_path = os.path.join(dest, rel_path)

                # clarify status for over(writing)
                file2write = os.path.join(dest_path, file)
                file_exists = (os.path.exists(file2write))
                do_writing = file_exists and overwrite or not file_exists
                if do_writing:

                    if not os.path.isdir(dest_path):
                        os.makedirs(dest_path)

                    # do it. with file metadata (copy2)
                    shutil.copy2(os.path.join(root, file), file2write)



if __name__ == '__main__':
    pass