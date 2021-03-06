#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cdgprofilergenestoterm
----------------------------------

Tests for `cdgprofilergenestoterm` module.
"""

import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import MagicMock
import pandas as pd

from cdgprofilergenestoterm import cdgprofilergenestotermcmd


class TestCdgprofilergenestoterm(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_inputfile(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('hellothere')
            res = cdgprofilergenestotermcmd.read_inputfile(tfile)
            self.assertEqual('hellothere', res)
        finally:
            shutil.rmtree(temp_dir)

    def test_parse_args(self):
        myargs = ['inputarg']
        res = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                         myargs)
        self.assertEqual('inputarg', res.input)
        self.assertEqual(0.00000001, res.maxpval)
        self.assertEqual(0.05, res.minoverlap)
        self.assertEqual('hsapiens', res.organism)
        self.assertEqual(500, res.maxgenelistsize)

    def test_run_gprofiler_no_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            try:
                cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                        theargs)
                self.fail('Expected FileNotFoundError')
            except FileNotFoundError:
                pass
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_empty_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')
            open(tfile, 'a').close()
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs)
            self.assertEqual(None, res)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_empty_result(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()
            mygprofiler.profile = MagicMock(return_value=pd.DataFrame())
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper
                                                          =mygprofiler)
            self.assertEqual(None, res)
            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=False)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_too_many_genes(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')

            # write out gene file with 5002 genes which
            # should return None
            with open(tfile, 'w') as f:
                for x in range(0, 5001):
                    f.write(str(x) + ',')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs)
            self.assertEqual(None, res)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_empty_result(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()

            df = pd.DataFrame()
            mygprofiler.profile = MagicMock(return_value=df)
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c,')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper=
                                                          mygprofiler)
            self.assertEqual(None, res)

            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=False)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_no_result_meeting_minoverlap(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()

            df = pd.DataFrame(columns=['name',
                                       'source',
                                       'native',
                                       'p_value',
                                       'description',
                                       'intersections',
                                       'precision',
                                       'recall',
                                       'term_size'],
                              data=[['name1',
                                     'source1',
                                     'native1',
                                     0.1,
                                     'desc1',
                                     ['hi'],
                                     0.5,
                                     0.7, 88],
                                    ['name2',
                                     'source2',
                                     'native2',
                                     0.5,
                                     'desc2',
                                     ['bye'],
                                     0.6,
                                     0.8, 99]])
            mygprofiler.profile = MagicMock(return_value=df)
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c,')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            theargs.minoverlap=0.6

            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper=
                                                          mygprofiler)
            self.assertEqual(None, res)

            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=False)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_no_result_cause_sources_in_exclude_list(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()

            df = pd.DataFrame(columns=['name',
                                       'source',
                                       'native',
                                       'p_value',
                                       'description',
                                       'intersections',
                                       'precision',
                                       'recall',
                                       'term_size'],
                              data=[['name1',
                                     'TF',
                                     'native1',
                                     0.1,
                                     'desc1',
                                     ['hi'],
                                     0.5,
                                     0.7, 88],
                                    ['name2',
                                     'MIRNA',
                                     'native2',
                                     0.5,
                                     'desc2',
                                     ['bye'],
                                     0.6,
                                     0.8, 99],
                                    ['name2',
                                     'HP',
                                     'native2',
                                     0.5,
                                     'desc2',
                                     ['bye'],
                                     0.6,
                                     0.8, 99]
                                    ])
            mygprofiler.profile = MagicMock(return_value=df)
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c,')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)

            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper=
                                                          mygprofiler)
            self.assertEqual(None, res)

            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=False)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_valid_result(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()

            df = pd.DataFrame(columns=['name',
                                       'source',
                                       'native',
                                       'p_value',
                                       'description',
                                       'intersections',
                                       'precision',
                                       'recall',
                                       'term_size'],
                              data=[['name1',
                                     'source1',
                                     'native1',
                                     0.1,
                                     'desc1',
                                     ['hi'],
                                     0.5,
                                     0.7, 88],
                                    ['name2',
                                     'source2',
                                     'native2',
                                     0.5,
                                     'desc2',
                                     ['bye'],
                                     0.6,
                                     0.8, 99]])
            mygprofiler.profile = MagicMock(return_value=df)
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c,')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper=
                                                          mygprofiler)
            self.assertEqual('name2', res['name'])
            self.assertEqual(['bye'], res['intersections'])
            self.assertEqual(99, res['term_size'])
            self.assertEqual(0.5, res['p_value'])
            self.assertEqual('source2', res['source'])
            self.assertEqual('native2', res['sourceTermId'])
            self.assertEqual(0.522, res['jaccard'])

            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=False)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_gprofiler_with_valid_no_intersections_in_result(self):
        temp_dir = tempfile.mkdtemp()
        try:
            mygprofiler = MagicMock()

            df = pd.DataFrame(columns=['name',
                                       'source',
                                       'native',
                                       'p_value',
                                       'description',
                                       'intersections',
                                       'precision',
                                       'recall',
                                       'term_size'],
                              data=[['name1',
                                     'source1',
                                     'native1',
                                     0.1,
                                     'desc1',
                                     ['hi'],
                                     0.5,
                                     0.7, 88],
                                    ['name2',
                                     'source2',
                                     'native2',
                                     0.5,
                                     'desc2',
                                     ['bye'],
                                     0.6,
                                     0.8, 99]])
            mygprofiler.profile = MagicMock(return_value=df)
            tfile = os.path.join(temp_dir, 'foo')
            with open(tfile, 'w') as f:
                f.write('a,b,c,')
            myargs = [tfile]
            theargs = cdgprofilergenestotermcmd._parse_arguments('desc',
                                                                 myargs)
            theargs.omit_intersections = True
            res = cdgprofilergenestotermcmd.run_gprofiler(tfile,
                                                          theargs,
                                                          gprofwrapper=
                                                          mygprofiler)
            self.assertEqual('name2', res['name'])
            self.assertEqual([], res['intersections'])
            self.assertEqual(99, res['term_size'])
            self.assertEqual(0.5, res['p_value'])
            self.assertEqual('source2', res['source'])
            self.assertEqual('native2', res['sourceTermId'])
            self.assertEqual(0.522, res['jaccard'])

            mygprofiler.profile.assert_called_once_with(query=['a', 'b', 'c'],
                                                        domain_scope='known',
                                                        organism='hsapiens',
                                                        user_threshold=0.00000001,
                                                        no_evidences=True)
        finally:
            shutil.rmtree(temp_dir)

    def test_main_invalid_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')
            myargs = ['prog', tfile]
            res = cdgprofilergenestotermcmd.main(myargs)
            self.assertEqual(2, res)
        finally:
            shutil.rmtree(temp_dir)

    def test_main_empty_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            tfile = os.path.join(temp_dir, 'foo')
            open(tfile, 'a').close()
            myargs = ['prog', tfile]
            res = cdgprofilergenestotermcmd.main(myargs)
            self.assertEqual(0, res)
        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    sys.exit(unittest.main())
