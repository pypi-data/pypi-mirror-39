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


import unittest
import os
import glob
import shutil

from geopathfinder.folder_naming import SmartPath
from geopathfinder.folder_naming import NullSmartPath
from geopathfinder.sgrt_naming import sgrt_tree

def cur_path():
    pth, _ = os.path.split(os.path.abspath(__file__))
    return pth


def get_test_sp(root,
                sensor=None,
                mode=None,
                group=None,
                datalog=None,
                product=None,
                wflow=None,
                grid=None,
                tile=None,
                var=None,
                qlook=True,
                make_dir=False):
    '''
    Function creating a SmartPath() for testing SmartPath().
    '''


    # defining the levels in the directory tree (order could become shuffled around)
    levels = {'root': root,
              'sensor': sensor,
              'mode': mode,
              'group': group,
              'datalog': datalog,
              'product': product,
              'wflow': wflow,
              'grid': grid,
              'tile': tile,
              'var': var,
              'qlook': 'qlooks'}

    # defining the hierarchy
    hierarchy = ['root', 'sensor', 'mode', 'group',
                 'datalog', 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    return SmartPath(levels, hierarchy, make_dir=make_dir)


def get_test_sp_4_smarttree(sensor=None,
                mode=None,
                group=None,
                datalog=None,
                product=None,
                wflow=None,
                grid=None,
                tile=None,
                var=None,
                qlook=True,
                make_dir=False):
    '''
    Function creating a SmartPath() for testing SmartTree().
    '''


    # defining the levels in the directory tree (order could become shuffled around)
    levels = {'sensor': sensor,
              'mode': mode,
              'group': group,
              'datalog': datalog,
              'product': product,
              'wflow': wflow,
              'grid': grid,
              'tile': tile,
              'var': var,
              'qlook': 'qlooks'}

    # defining the hierarchy
    hierarchy = ['sensor', 'mode', 'group',
                 'datalog', 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    return SmartPath(levels, hierarchy, make_dir=make_dir)


class TestSmartPath(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(cur_path(), 'test_temp_dir')
        self.sp_obj = get_test_sp(self.path, sensor='Sentinel-1_CSAR',
                                  mode='IWGRDH', group='products',
                                  datalog='datasets', product='ssm',
                                  wflow='C1003', grid='EQUI7_EU500M',
                                  tile='E048N012T6', var='ssm',
                                  make_dir=True)

        self.path_perm = os.path.join(cur_path(), 'test_data')
        self.sp_obj_perm = get_test_sp(self.path_perm,
                                       sensor='Sentinel-1_CSAR',
                                       mode='IWGRDH', group='products',
                                       datalog='datasets', product='ssm',
                                       wflow='C1003', grid='EQUI7_EU500M',
                                       tile='E048N012T6', var='ssm',
                                       make_dir=True)

    def tearDown(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)


    def test_get_dir(self):
        '''
        Testing the creation of the directory.

        '''
        result = self.sp_obj.get_dir(make_dir=True)

        assert os.path.exists(result)


    def test_build_levels(self):
        '''
        Testing the level creation.

        '''
        should = os.path.join(self.path, 'Sentinel-1_CSAR', 'IWGRDH', 'products',
                              'datasets', 'ssm', 'C1003')

        result = self.sp_obj.build_levels(level='wflow', make_dir=True)

        assert should == result

        assert os.path.exists(result)


    def test_get_level(self):
        '''
        Testing the level query.

        '''
        should = os.path.join(self.path, 'Sentinel-1_CSAR', 'IWGRDH')

        result = self.sp_obj['mode']

        assert should == result


    def test_expand_full_path(self):
        '''
        Testing the path expansion

        '''
        should = [os.path.join(self.path, 'Sentinel-1_CSAR', 'IWGRDH', 'MY_TEST.txt')]

        result = self.sp_obj.expand_full_path('mode', ['MY_TEST.txt'])

        assert should == result


    def test_search_files(self):
        '''
        Testing the file search yielding file lists.

        '''
        should = ['M20161218_051642--_SSM------_S1BIWGRDH1VVD_095_C1003_EU500M_E048N012T6.tif',
                  'M20170406_050911--_SSM------_S1AIWGRDH1VVD_022_C1003_EU500M_E048N012T6.tif']

        src = glob.glob(os.path.join(cur_path(), 'test_data', '*.*'))
        dest = self.sp_obj.build_levels(level='var', make_dir=True)

        for file in src:
            shutil.copy(file, dest)

        result = self.sp_obj.search_files('var', pattern='SSM')

        assert should == result


    def test_build_file_register(self):
        '''
        Testing the file register.

        '''

        self.sp_obj_perm.build_file_register(level='var')

        self.assertEqual(self.sp_obj_perm.file_count, 5)


class TestSmartTree(unittest.TestCase):
    """
    Tests function of the SmartTree() class, applied for testing to the
    SGRT convention.

    """
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), os.path.join('test_data', 'Sentinel-1_CSAR'))
        self.copy_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), os.path.join('test_data', 'copy_target'))
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        os.mkdir(self.copy_dir)
        self.stt_1 = sgrt_tree(self.test_dir, register_file_pattern='.tif')


    def tearDown(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)


    def test_tree_integrity(self):
        """
        Tests of only valid paths are added to the SmartTree()

        """
        self.assertTrue(
            all([True for x in self.stt_1.get_all_dirs() if self.test_dir in x]))


    def test_tree_dir_n_file_count(self):
        """
        Tests the dir_ and file_count of SmartTree()

        """
        self.assertEqual(self.stt_1.dir_count, 9)
        self.assertEqual(self.stt_1.file_count, 17)
        # TODO: should be 16 "file_too_deep.tif" should be not included in
        # file_register!


    def test_get_smartpath(self):
        """
        Tests the selection of a SmartPath matching regex search patterns.

        """
        # typical use case
        should = ['M20160831_163321--_SIG0-----_S1AIWGRDH1VVA_175_A0201_EU500M_E048N006T6.tif']
        result = self.stt_1.get_smartpath(('A0202', 'sig0')).search_files(
            level='var')
        self.assertEqual(should, result)

        # typical use case
        should = ['Q20160831_163321--_SIG0-----_S1AIWGRDH1VVA_175_A0201_EU500M_E006N006T6.tif']
        result = self.stt_1[('A0202', 'sig0')].search_files(level='qlook')
        self.assertEqual(should, result)

        # test postive search pattern
        should = os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets', 'ssm', 'C1003', 'EQUI7_EU500M', 'E048N012T6', 'ssm-noise', 'qlooks')
        result = self.stt_1.get_smartpath(('C1003', 'E048N012T6', 'noise')).get_dir()
        self.assertEqual(should, result)

        # test negative search pattern
        should = os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets', 'ssm', 'C1003', 'EQUI7_EU500M', 'E048N012T6', 'ssm', 'qlooks')
        result = self.stt_1['C1003', 'E048N012T6', '-noise'].get_dir()
        self.assertEqual(should, result)

        # handling of no matches
        self.assertTrue(isinstance(self.stt_1['nonsense'], NullSmartPath))

        # handling of multiple matches
        self.assertTrue(isinstance(self.stt_1['A0202'], NullSmartPath))


    def test_collect_level(self):
        """
        Test the collect level functions

        """

        # unique case for the folder topnames
        should = ['E006N006T1', 'E006N006T6', 'E006N006T6',
                  'E006N006T6', 'E006N012T6', 'E048N012T6']
        result = sorted(self.stt_1.collect_level_topnames('tile', unique=True))
        self.assertEqual(should, result)

        # non-unique case for the folder topnames
        should = ['E006N006T1', 'E006N006T6', 'E006N006T6',
                  'E006N006T6', 'E006N006T6', 'E006N012T6',
                  'E048N012T6', 'E048N012T6']
        result = sorted(self.stt_1.collect_level_topnames('tile', unique=False))
        self.assertEqual(should, result)

        # unique case for full dirs
        should = [os.path.join(self.test_dir, 'IWGRDH', 'preprocessed', 'datasets', 'resampled', 'A0202', 'EQUI7_EU500M'),
                  os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets', 'ssm', 'C1001', 'EQUI7_AF010M'),
                  os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets', 'ssm', 'C1001', 'EQUI7_EU500M'),
                  os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets', 'ssm', 'C1003', 'EQUI7_EU500M')]
        result = sorted(self.stt_1.collect_level('grid', unique=True))
        self.assertEqual(should, result)

        # test if unique full dirs deliver correct number of topnames
        should = ['EQUI7_AF010M',
                  'EQUI7_EU500M',
                  'EQUI7_EU500M',
                  'EQUI7_EU500M']
        result = sorted(self.stt_1.collect_level_topnames('grid', unique=True))
        self.assertEqual(should, result)


    def test_trim2branch(self):
        """
        Test the function for returning a branch (subtree).

        """

        branch1 = self.stt_1.trim2branch('wflow', 'C1003', register_file_pattern='.')
        self.assertEqual(branch1.collect_level_topnames('root'), ['C1003'])

        self.assertEqual(branch1.dir_count, 4)
        self.assertEqual(len(branch1.file_register), 12)
        self.assertEqual(branch1.file_count, 12)

        should = ['E006N006T6', 'E006N012T6', 'E048N012T6']
        self.assertEqual(sorted(branch1.collect_level_topnames('tile')), should)

        # handling of multiple matches
        branch2 = self.stt_1.trim2branch('grid', 'EQUI7_EU500M')
        self.assertEqual(branch2.dir_count, 0)
        self.assertEqual(len(branch2.file_register), 0)
        self.assertEqual(branch2.file_count, 0)


    def test_copy_smarttree_on_fs(self):
        """
        Tests if the copy functions works properly.

        """
        self.stt_1.copy_smarttree_on_fs(self.copy_dir)

        files = next(os.walk(self.copy_dir))[2]
        file_count = sum([len(files) for r, d, files in os.walk(self.copy_dir)])

        self.assertEqual(file_count, 24)


    def test_copy_smarttree_on_fs_level_pattern(self):
        """
        Tests if the copy functions works properly for given level and pattern.

        """
        self.stt_1.copy_smarttree_on_fs(self.copy_dir,
                                        level='wflow', level_pattern='A0202')

        files = next(os.walk(self.copy_dir))[2]
        file_count = sum(
            [len(files) for r, d, files in os.walk(self.copy_dir)])

        self.assertEqual(file_count, 4)




if __name__ == "__main__":
    unittest.main()
