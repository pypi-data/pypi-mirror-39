# -*- coding: utf-8 -*-

###############################################################################
import numpy as np 
import os
import unittest

from ono.bruker_opus_filereader import OpusReader

### local imports from ########################################################
from semi.carbon_concentration.carbon_report import ReportGenerator

###############################################################################
class TestReportGenerator(unittest.TestCase):

    data = {}
    logo = 'data\\logo.pdf'

    @classmethod
    def setUpClass(cls):
        testdir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.join(testdir, '..'))
        datadir = os.path.join(basedir, 'data')

        filename = 'I1625_20_Diff_2017_02_27_10_20.0'
        fullfile = os.path.join(datadir, filename)
        
        cls.sample = OpusReader(fullfile)
        cls.sample.readDataBlocks()

        fxv = cls.sample['AB Data Parameter']['FXV']
        lxv = cls.sample['AB Data Parameter']['LXV']
        npt = cls.sample['AB Data Parameter']['NPT']
        wn = np.linspace(fxv, lxv, npt)
        absorption = cls.sample['AB']

        cls.data = {
            'absorption': absorption,
            'absorption_peak_height': "0.367 cm<super>-1</super>",
            'absorption_peak_width': "1.6 cm<super>-1</super>",
            'apertur': '2 mm',
            'carbon': '7.52E+15 cm<super>-3</super>',
            'date': '01.01.2018',
            'detector': 'MCT',
            'number_of_scans': str(32),
            'peak_amplitude': str(-7149),
            'peak_position': str(60527),
            'position': str(2),
            'residuum': str(0.0061),
            'resolution': '0.75 cm<super>-1</super>',
            'sample': 'A1234/K1',
            'sample_thickness': '10.29 mm',
            'scan_velocity': '40 kHz',
            'time': "11:11",
            'wn': wn,
        }


    def test_00_generate(self):

        report = ReportGenerator(
            TestReportGenerator.data,
            logo=TestReportGenerator.logo)
        
        error = report.generate('output\\test.pdf')

        self.assertEqual(error, 0)
        

    def test_01_exception(self):
        report = ReportGenerator(
            TestReportGenerator.data,
            logo=TestReportGenerator.logo)
        
        report.generate('wrong_directory\\test.pdf')        

