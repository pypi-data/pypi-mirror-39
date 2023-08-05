from obspy import read, read_events
from eqcorrscan.core import template_gen
from eqcorrscan.utils.plotting import pretty_template_plot
import os
test_file = os.path.realpath('../../..') +             '/tests/test_data/REA/TEST_/01-0411-15L.S201309'
test_wavefile = os.path.realpath('../../..') +            '/tests/test_data/WAV/TEST_/' +            '2013-09-01-0410-35.DFDPC_024_00'
event = read_events(test_file)[0]
st = read(test_wavefile)
st.filter('bandpass', freqmin=2.0, freqmax=15.0)
for tr in st:
    tr.trim(tr.stats.starttime + 30, tr.stats.endtime - 30)
    tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]
template = template_gen._template_gen(event.picks, st, 2)
pretty_template_plot(template, background=st,
                     picks=event.picks)