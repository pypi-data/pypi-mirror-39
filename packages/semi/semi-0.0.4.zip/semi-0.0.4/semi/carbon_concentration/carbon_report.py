# -*- coding: utf-8 -*-

### imports ###################################################################
import logging
import sys

###############################################################################
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus.tables import Table
# from reportlab.lib import colors

### local imports #############################################################
from some_reportlab_snippets.mplfig import MatplotlibFig
from some_reportlab_snippets.report import Report

###############################################################################
class ReportGenerator():
    """
    Class to generate a pdf report.
    """
    def __init__(self, data, **kwargs):
        self.data = data
        
        self.report = Report(**kwargs)
        self.spacer = Spacer(1, 10)

        self.table_style = [
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]

        self.setHeadline()
        self.setInstrumentTable()
        self.setJobTable()
        self.setMeasurementTable()
        self.setResultTable()
        self.setSpectrum()

        table_content = [[self.instrument_table, self.measurement_table],]

        self.combined_table = Table(
                table_content, repeatRows=0, style=self.table_style)
        
        
        content_list = [
            self.headline,
            self.job_table,
            self.spacer,
            self.result_table,
            self.spacer,
            self.combined_table,
            # self.instrument_table,
            # self.spacer,
            # self.measurement_table,
            self.spacer,
            self.spectrum
        ]
        
        
        self.report.story = content_list
        

    def generate(self, reportfile = "test.pdf"):
        """
        The actual pdf generation.
        """
        error = 0

        try:
            self.report.save(reportfile)
        except FileNotFoundError:
            logging.error(
                "Error during report generation: %s, %s",
                sys.exc_info()[0],
                sys.exc_info()[1]
            )

            error = -1
        return error


    def getValue(self, valueStr):
        p = Paragraph(valueStr, self.report.styleSheet['BodyText'])
        return p
    

    def setHeadline(self):
        self.headline = Paragraph(
            "Kohlenstoffmessung",
            style = self.report.styleSheet['Title'])


    def setInstrumentTable(self):
        table_headline = Paragraph(
            "<strong>Instrumentenparameter</strong>",
            self.report.styleSheet['Normal'])

        table_content = [
            [table_headline],
            ["Spektrometer:", "VERTEX 77"],
            ["Maschinen-Nr.:", "RM402"],
            [""],
            ["Peakamplitude:", self.data['peak_amplitude']],
            ["Peakposition:", self.data['peak_position']],
            [""],
            ["Detektor:", self.data['detector']],
            ["Apertur:", self.data['apertur']],
            [""],
            ["Anzahl Scans:", self.data['number_of_scans']],
            ["Scan-Geschw.:", self.data['scan_velocity']],
            ["Auflösung", self.getValue(self.data['resolution'])],]

        self.instrument_table = Table(
            table_content,
            repeatRows = 0,
            style = self.table_style + [
                # ('LINEBEFORE', (2, 1), (2, -1), 1.2, colors.black),
                # ('SPAN', (1, -1), (-1, -1))
            ]
        )


    def setJobTable(self):
        table_headline = Paragraph(
            "<strong>Auftragsdaten</strong>",
            self.report.styleSheet['Normal'])

        table_content = [
            [table_headline],
            ["Probe:", self.data['sample']],]

        self.job_table = Table(
            table_content,
            repeatRows = 0,
            style = self.table_style + [
                # ('LINEBEFORE', (2, 1), (2, -1), 1.2, colors.black),
                # ('SPAN', (1, -1), (-1, -1))
            ]
        )


    def setMeasurementTable(self):
        table_headline = Paragraph(
            "<strong>Messparameter</strong>",
            self.report.styleSheet['Normal'])

        abs_peak_height = self.getValue(self.data['absorption_peak_height'])
        abs_peak_width = self.getValue(self.data['absorption_peak_width'])
        
        table_content = [
            [table_headline],
            ["Probendicke:", self.data['sample_thickness']],
            ["max. Abs.-Koeff.:", abs_peak_height],
            ["Halbwertsbreite:", abs_peak_width],
            ["RMS-Residuum:", self.data['residuum']],
            [""],
            ["Datum:", self.data['date']],
            ["Zeit:", self.data['time']],
            [""],
            ["Experiment", "MCT, KBr-BMS, Globar"],
            ["Probenpos.:", self.data['position']],]

        self.measurement_table = Table(
            table_content,
            repeatRows = 0,
            style = self.table_style + [
                # ('LINEBEFORE', (2, 1), (2, -1), 1.2, colors.black),
                # ('SPAN', (1, -1), (-1, -1))
            ]
        )


    def setResultTable(self):
        table_headline = [Paragraph(
            "<strong>Messergebnis</strong>",
            self.report.styleSheet['Normal']
        ),]

        result_line = ["Kohlenstoffgehalt:",
             Paragraph(
                     "<strong>" + self.data['carbon'] + "</strong>",
                     self.report.styleSheet['BodyText'])]
             
        table_content = [table_headline, result_line]

        self.result_table = Table(
            table_content, repeatRows = 0, style = self.table_style
        )
        
    
    def setSpectrum(self):
        figsize = (6, 4.5)
        fig = MatplotlibFig(figsize=figsize)
        
        x = self.data['wn']
        y = self.data['absorption']
        
        fig.setData(x, y)
        
        fig.xlim = (600, 565)
        fig.xlabel = 'Wellenzahl [cm$^{-1}$]'
        fig.ylabel = 'Absorptionskoeffizient [cm$^{-1}$]'
        
        self.spectrum = fig.savefig()
        
