#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trx Wide Template
# Generated: Thu Dec 19 09:25:17 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy
import red_pitaya_wide
import sys


class trx_wide_template(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Trx Wide Template")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Trx Wide Template")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "trx_wide_template")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.tx_samp_rate = tx_samp_rate = 1250000
        self.ptt = ptt = False
        self.noise_volt = noise_volt = 0.000100
        self.ampl = ampl = 0.5
        self.addr = addr = "192.168.1.100"
        
        self.QPSK = QPSK = digital.constellation_calcdist(([(-1-1j),(-1+1j),(1+1j),(1-1j)]), ([0, 1, 3, 2]), 4, 1).base()
        

        ##################################################
        # Blocks
        ##################################################
        _ptt_check_box = Qt.QCheckBox("ptt")
        self._ptt_choices = {True: True, False: False}
        self._ptt_choices_inv = dict((v,k) for k,v in self._ptt_choices.iteritems())
        self._ptt_callback = lambda i: Qt.QMetaObject.invokeMethod(_ptt_check_box, "setChecked", Qt.Q_ARG("bool", self._ptt_choices_inv[i]))
        self._ptt_callback(self.ptt)
        _ptt_check_box.stateChanged.connect(lambda i: self.set_ptt(self._ptt_choices[bool(i)]))
        self.top_grid_layout.addWidget(_ptt_check_box, 0,0,1,1)
        self._ampl_range = Range(0, 4, 0.025, 0.5, 200)
        self._ampl_win = RangeWidget(self._ampl_range, self.set_ampl, 'ampli', "counter_slider", float)
        self.top_layout.addWidget(self._ampl_win)
        self.t4t = blocks.multiply_const_vcc((ampl, ))
        self.red_pitaya_wide_sink_1 = red_pitaya_wide.sink(
                addr='192.168.1.100',
                port=1001,
                freq=0,
                rate=tx_samp_rate,
                mask=3,
                corr=0,
                ptt=True
        )
          
        self._noise_volt_range = Range(0, 1, 0.01, 0.000100, 200)
        self._noise_volt_win = RangeWidget(self._noise_volt_range, self.set_noise_volt, 'noise_voltage', "counter_slider", float)
        self.top_layout.addWidget(self._noise_volt_win)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=QPSK,
          differential=True,
          samples_per_symbol=25,
          pre_diff_code=True,
          excess_bw=0.88,
          verbose=False,
          log=False,
          )
        self.analog_random_source_x_1 = blocks.vector_source_b(map(int, numpy.random.randint(0, 2, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_1, 0), (self.digital_constellation_modulator_0, 0))    
        self.connect((self.digital_constellation_modulator_0, 0), (self.t4t, 0))    
        self.connect((self.t4t, 0), (self.red_pitaya_wide_sink_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "trx_wide_template")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.red_pitaya_wide_sink_1.set_rate(self.tx_samp_rate)

    def get_ptt(self):
        return self.ptt

    def set_ptt(self, ptt):
        self.ptt = ptt
        self._ptt_callback(self.ptt)

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.t4t.set_k((self.ampl, ))

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK


def main(top_block_cls=trx_wide_template, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
