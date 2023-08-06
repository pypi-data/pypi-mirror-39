from itertools import chain
from nose.tools import assert_raises, eq_, assert_greater

from eelbrain import datasets, plot
from eelbrain.plot import _base
from eelbrain.plot._base import Layout
from eelbrain._utils.testing import skip_on_windows


def assert_layout_ok(*args, **kwargs):
    error = None
    l = Layout(*args, **kwargs)
    if l.nrow * l.ncol < l.nax:
        error = ("%i rows * %i cols = %i < %i (nax). args=%%r, kwargs=%%r"
                 % (l.nrow, l.ncol, l.nrow * l.ncol, l.nax))

    if error:
        raise AssertionError(error % (args, kwargs))


def test_layout():
    "Test the Layout class"
    for nax in range(1, 100):
        assert_layout_ok(nax, 1.5, 2, True, w=5)
        assert_layout_ok(nax, 1.5, 2, True, h=5)
        assert_layout_ok(nax, 1.5, 2, True, axw=5)
        assert_layout_ok(nax, 1.5, 2, True, axh=5)
        assert_layout_ok(nax, 1.5, 2, True, axw=5, w=20)
        assert_layout_ok(nax, 1.5, 2, True, axw=5, h=20)
        assert_layout_ok(nax, 1.5, 2, True, axh=5, w=20)
        assert_layout_ok(nax, 1.5, 2, True, axh=5, h=20)

    # single axes larger than figure
    assert_raises(ValueError, Layout, 2, 1.5, 2, True, h=5, axh=6)
    assert_raises(ValueError, Layout, 2, 1.5, 2, True, w=5, axw=6)

    # left margin & axw
    margins = dict(left=1, top=2, bottom=1, wspace=1, hspace=2)
    layout = Layout(2, 2, 2, margins=margins, axw=5, w=10, ncol=1)
    assert layout.w == 10
    assert layout.margins == dict(right=10 - 1 - 5, **margins)
    assert layout.axh == 2.5
    assert layout.h == 5 + 2 * layout.axh


def test_time_slicer():
    "Test linked time axes"
    ds = datasets.get_uts(True)

    p1 = plot.Butterfly(ds['utsnd'], show=False)
    p2 = plot.Array('utsnd', 'A', ds=ds, show=False)
    p1.link_time_axis(p2)

    p1._set_time(.1, True)
    assert p2._current_time == .1
    assert p2._time_fixed == True
    p2._set_time(.2)
    assert p1._current_time == .2
    assert p1._time_fixed == False

    p1 = plot.TopoButterfly(ds['utsnd'], show=False)
    p2 = plot.Array('utsnd', 'A', ds=ds, show=False)
    p2.link_time_axis(p1)

    p1._set_time(.1, True)
    assert p2._current_time == .1
    assert p2._time_fixed == True

    # merge another
    p3 = plot.TopoButterfly(ds[0, 'utsnd'], show=False)
    p3.link_time_axis(p2)

    p2._set_time(.2)
    assert p1._current_time == .2
    assert p1._time_fixed == False


def test_vlims():
    "Test vlim determination"
    ds = datasets.get_uts()
    epochs = [[ds[i: i+5, 'uts'].mean('case')] for i in range(0, 10, 5)]
    meas = ds['uts'].info.get('meas')

    lims = _base.find_fig_vlims(epochs)
    assert_greater(lims[meas][1], lims[meas][0])
    lims = _base.find_fig_vlims(epochs, 1)
    eq_(lims[meas], (-1, 1))
    lims = _base.find_fig_vlims(epochs, 1, -2)
    eq_(lims[meas], (-2, 1))

    # positive data
    epochs = [[e * e.sign()] for e in chain(*epochs)]
    lims = _base.find_fig_vlims(epochs)
    eq_(lims[meas][0], 0)
    lims = _base.find_fig_vlims(epochs, 1)
    eq_(lims[meas], (0, 1))
    lims = _base.find_fig_vlims(epochs, 1, -1)
    eq_(lims[meas], (-1, 1))

    # symmetric
    cmaps = _base.find_fig_cmaps(epochs)
    eq_(cmaps, {meas: 'xpolar'})
    lims = _base.find_fig_vlims(epochs, cmaps=cmaps)
    eq_(lims[meas][0], -lims[meas][1])
    lims = _base.find_fig_vlims(epochs, 1, cmaps=cmaps)
    eq_(lims[meas], (-1, 1))
    lims = _base.find_fig_vlims(epochs, 1, 0, cmaps=cmaps)
    eq_(lims[meas], (-1, 1))

    # zero-based
    cmaps[meas] = 'sig'
    lims = _base.find_fig_vlims(epochs, cmaps=cmaps)
    eq_(lims[meas][0], 0)
    lims = _base.find_fig_vlims(epochs, 1, cmaps=cmaps)
    eq_(lims[meas], (0, 1))
    lims = _base.find_fig_vlims(epochs, 1, -1, cmaps=cmaps)
    eq_(lims[meas], (0, 1))


@skip_on_windows  # window resizes to screen size
def test_eelfigure():
    ds = datasets.get_uts()

    p = plot.UTSStat('uts', 'A', ds=ds, h=2, w=50, show=False)
    eq_(tuple(p.figure.get_size_inches()), (50, 2))
