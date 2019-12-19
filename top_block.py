#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Dec 19 09:21:55 2019
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
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import red_pitaya_wide
import sip
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.tx_samp_rate = tx_samp_rate = 100000
        self.samp_rate = samp_rate = 100000
        self.rx_samp_rate = rx_samp_rate = 100000
        self.ptt = ptt = False
        self.addr = addr = "192.168.1.100"

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
        self.red_pitaya_wide_source_0 = red_pitaya_wide.source(
                addr=str(addr),
                port=1001,
                freq=0,
                rate=rx_samp_rate,
                mask=3,
                corr=0
        )
          
        self.red_pitaya_wide_sink_0 = red_pitaya_wide.sink(
                addr='192.168.1.100',
                port=1001,
                freq=0,
                rate=tx_samp_rate,
                mask=3,
                corr=0,
                ptt=True
        )
          
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	rx_samp_rate, #bw
        	'QT GUI Plot', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1,0,1,1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 2, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.red_pitaya_wide_sink_0, 0))    
        self.connect((self.red_pitaya_wide_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.red_pitaya_wide_sink_0.set_rate(self.tx_samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.red_pitaya_wide_source_0.set_rate(self.rx_samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.rx_samp_rate)

    def get_ptt(self):
        return self.ptt

    def set_ptt(self, ptt):
        self.ptt = ptt
        self._ptt_callback(self.ptt)

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr


def main(top_block_cls=top_block, options=None):

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
