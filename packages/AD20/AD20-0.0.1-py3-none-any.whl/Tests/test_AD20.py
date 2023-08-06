import pytest
import AD20
import numpy as np
import networkx as nx
import matplotlib
import pandas
from AD20.ADnum import ADnum
from AD20 import ADmath as ADmath
from AD20 import ADgraph

#ADnum unit tests
def test_ADnum_init():
    x = ADnum(100, der = -2)
    assert x.val == 100
    assert x.der == -2
    assert len(x.graph)==0

def test_ADnum_valtype():
    with pytest.raises(ValueError):
        z = ADnum('zoo', der = 1)

def test_ADnum_dertype():
    with pytest.raises(ValueError):
        z = ADnum(3.0, der = 'zebra')

def test_ADnum_nodernoins():
    with pytest.raises(Exception):
        z = ADnum(4, ind = 0)


def test_ADnum_nodernoind():
    with pytest.raises(Exception):
        z = ADnum(4, ins = 3)

def test_ADnum_nodernothing():
    with pytest.raises(Exception):
        z = ADnum(3)

def test_ADnum_derconsistent():
    with pytest.raises(ValueError):
        z = ADnum(3, der = np.array([1, 3]), ins = 5)

def test_graphiput():
    z = ADnum(1, der = 1, graph = {'a': 1})
    assert z.graph == {'a':1}

def test_neg():
    x = ADnum(4, der =1)
    f = -x
    assert f.val == -4.0
    assert f.der == -1.0
    assert len(f.graph)==1

def test_ADnum_mul():
    x = ADnum(3.0, der = 1)
    f = x*2.0
    assert f.val == 6.0
    assert f.der == 2.0
    assert len(f.graph) == 2

def test_ADnum_rmul():
    x = ADnum(3.0, der = 1)
    f = 2.0*x
    assert f.val == 6.0
    assert f.der == 2.0
    assert len(f.graph) == 2

def test_ADnum_add():
    x = ADnum(3.0, der = 1)
    f = x+2.0
    assert f.val == 5.0
    assert f.der == 1.0
    assert len(f.graph) == 2

def test_ADnum_radd():
    x = ADnum(3.0, der = 1)
    f = 2.0+x
    assert f.val == 5.0
    assert f.der == 1.0
    assert len(f.graph) == 2

def test_ADnum_sub():
    x = ADnum(5.0, der = 1)
    f = x-2.0
    assert f.val == 3.0
    assert f.der == 1.0
    assert len(f.graph) == 2

def test_ADnum_rsub():
    x = ADnum(3.0, der = 1)
    f = 5.0-x
    assert f.val == 2.0
    assert f.der == -1.0
    assert len(f.graph) == 2

def test_ADnum_div():
    x = ADnum(3.0, der = 1)
    f = x/1.5
    assert f.val == 2.0
    assert f.der == 1/1.5
    assert len(f.graph) == 2

def test_ADnum_rdiv():
    x = ADnum(3.0, der = 1)
    f = 6/x
    assert f.val == 2.0
    assert f.der == -2/3
    assert len(f.graph) == 2

def test_ADnum_pow():
    x = ADnum(3.0, der = 1)
    f = x**2.0
    assert f.val == 9.0
    assert f.der == 6.0
    assert len(f.graph) == 2

def test_ADnum_rpow():
    x = ADnum(3.0, der = 1)
    f = 4**x
    assert f.val == 64
    assert f.der == 64*np.log(4.0)
    assert len(f.graph) == 2

# ADmath unit tests

def test_ADmath_sin():
    X = ADnum(np.pi, der = 1)
    Y = ADmath.sin(X)
    assert Y.val == np.sin(np.pi)
    assert Y.der == np.cos(np.pi)
    assert len(Y.graph) == 1

def test_ADmath_cos():
    f = ADmath.cos(ADnum(4, der = 1))
    assert f.val == np.cos(4)
    assert f.der == -np.sin(4)
    assert len(f.graph) == 1

def test_ADmath_tan():
    f = ADmath.tan(ADnum(4, der = 1))
    assert f.val == np.tan(4)
    assert f.der == (1/np.cos(4))**2
    assert len(f.graph) == 1

def test_ADmath_csc():
    f = ADmath.csc(ADnum(5, der = 1))
    assert f.val == 1/np.sin(5)
    assert f.der == (-1/np.tan(5))*(1/np.sin(5))
    assert len(f.graph) == 1

def test_ADmath_sec():
    f = ADmath.sec(ADnum(6, der = 1))
    assert f.val == 1/np.cos(6)
    assert f.der == np.tan(6)/np.cos(6)
    assert len(f.graph) == 1

def test_ADmath_cot():
    f = ADmath.cot(ADnum(1, der = 1))
    assert f.val == 1/np.tan(1)
    assert f.der == -1/(np.sin(1)**2)
    assert len(f.graph) == 1

def test_ADmath_arcsin():
    f = ADmath.arcsin(ADnum(.2, der = 1))
    assert f.val == np.arcsin(.2)
    assert f.der == 1/(np.sqrt(1-.2**2))
    assert len(f.graph) == 1

def test_ADmath_arccos():
    f = ADmath.arccos(ADnum(.3, der = 1))
    assert f.val == np.arccos(.3)
    assert f.der == -1/(np.sqrt(1-.3**2))
    assert len(f.graph) == 1

def test_ADmath_arctan():
    f = ADmath.arctan(ADnum(1, der = 1))
    assert f.val == np.arctan(1)
    assert f.der == .5
    assert len(f.graph) == 1

def test_ADmath_sinh():
    f = ADmath.sinh(ADnum(2, der = 1))
    assert f.val == np.sinh(2)
    assert f.der == np.cosh(2)
    assert len(f.graph) == 1

def test_ADmath_cosh():
    f = ADmath.cosh(ADnum(3, der = 1))
    assert f.val == np.cosh(3)
    assert f.der == np.sinh(3)
    assert len(f.graph) == 1

def test_ADmath_tanh():
    f = ADmath.tanh(ADnum(-5, der = 1))
    assert f.val == np.tanh(-5)
    assert f.der == 1/(np.cosh(-5)**2)
    assert len(f.graph) == 1

def test_ADmath_exp():
    f = ADmath.exp(ADnum(-3, der = 1))
    assert f.val == np.exp(-3)
    assert f.der == np.exp(-3)
    assert len(f.graph) == 1

def test_ADmath_log():
    f = ADmath.log(ADnum(72, der = 1))
    assert f.val == np.log(72)
    assert f.der == 1/72
    assert len(f.graph) == 1

def test_ADmath_logistic():
    f = ADmath.logistic(ADnum(0, der=1))
    assert f.val == .5
    assert f.der == .25

def test_ADmath_sqrt():
    f = ADmath.sqrt(ADnum(40, der = 1))
    assert f.val == np.sqrt(40)
    assert f.der == 1/(2*np.sqrt(40))
    assert len(f.graph) == 1

def test_ADmath_sinr():
    X = np.pi
    Y = ADmath.sin(X)
    assert Y == np.sin(np.pi)


def test_ADmath_cosr():
    f = ADmath.cos(4)
    assert f == np.cos(4)

def test_ADmath_tanr():
    f = ADmath.tan(4)
    assert f == np.tan(4)

def test_ADmath_cscr():
    f = ADmath.csc(5)
    assert f == 1/np.sin(5)

def test_ADmath_secr():
    f = ADmath.sec(6)
    assert f == 1/np.cos(6)

def test_ADmath_cotr():
    f = ADmath.cot(1)
    assert f == 1/np.tan(1)

def test_ADmath_arcsinr():
    f = ADmath.arcsin(.2)
    assert f == np.arcsin(.2)

def test_ADmath_arccosr():
    f = ADmath.arccos(.3)
    assert f == np.arccos(.3)

def test_ADmath_arctanr():
    f = ADmath.arctan(1)
    assert f == np.arctan(1)

def test_ADmath_sinhr():
    f = ADmath.sinh(2)
    assert f == np.sinh(2)

def test_ADmath_coshr():
    f = ADmath.cosh(3)
    assert f == np.cosh(3)

def test_ADmath_tanhr():
    f = ADmath.tanh(-5)
    assert f == np.tanh(-5)

def test_ADmath_expr():
    f = ADmath.exp(-3)
    assert f == np.exp(-3)

def test_ADmath_logr():
    f = ADmath.log(72)
    assert f == np.log(72)

def test_ADmath_sqrtr():
    f = ADmath.sqrt(40)
    assert f == np.sqrt(40)

# More advanced tests
def test_12x():
    x = ADnum(1, der = 1)
    f = 1/(1-2*x)
    assert f.val == 1/(1-2)
    assert f.der == 2/(1-2)**2

def test_xex():
    x = ADnum(2, der = 1)
    f = x * ADmath.exp(x)
    assert f.val == 2.0 * np.exp(2.0)
    assert f.der == np.exp(2.0) + 2.0*np.exp(2.0)

def test_5x2lnx():
    x = ADnum(1, der = 1)
    f = 5 * x**2 * ADmath.log(x)
    assert f.val == 0.0
    assert f.der == 10 * 1.0 * np.log(1.0) + 5*1.0


def test_sinxcosx():
    x = ADnum(0, der = 1)
    f = ADmath.sin(x) * ADmath.cos(x)
    assert f.val == np.sin(0) * np.cos(0)
    assert f.der == -(np.sin(0) ** 2) + np.cos(0) **2

def test_2xe2x():
    x = ADnum(2, der = 1)
    f = 2 * x * ADmath.exp(2*x)
    assert f.val == 4 * np.exp(4)
    assert f.der == 2 * np.exp(4.0) + 8 * np.exp(4)

def test_multivar():
    x = ADnum(3, ins = 2, ind = 0) 
    y = ADnum(4, ins = 2, ind= 1)
    f = 2 * y + 2*x**2
    assert f.val == 2 * 4 + 2 * 3**2
    assert f.der.all() == np.all(np.array([12, 2]))

def test_vecinput():
    x = ADnum([1, 2, 3], ins = 1, ind = 0)
    assert np.array_equal(x.val, np.array([1., 2., 3.]))
    assert np.array_equal(x.der, np.array([1., 1., 1.]))

def test_vecinput_multi():
    x = ADnum([1, 2, 3], ins =2 , ind =0)
    assert np.array_equal(x.der, np.array([[1., 1., 1.],[0., 0., 0.]]))

#Graph testing
def test_gen_graph():
    d = {'y': [('x', 'test')]}
    Y = ADnum(1, der = 1, graph = d)
    G= ADgraph.gen_graph(Y)
    assert 'y' in G
    assert 'x' in G
    assert type(G) == nx.classes.digraph.DiGraph
    assert G.number_of_nodes()==2
    assert G.number_of_edges()==1

def test_reverse_graph():
    d = {'y': [('x', 'test')]}
    rd = {'x': [('y', 'test')]}
    Y = ADnum(1, der =1, graph = d)
    rg = ADgraph.reverse_graph(Y)
    assert rd == rg

def test_get_labels():
    X = ADnum(1, der =1)
    Y = ADmath.sin(X)+3
    labs = ADgraph.get_labels(Y)
    assert labs[X] == 'X0'
    assert labs[Y] == 'X2'
    assert len(labs) == 4

def test_get_colorsandsizes():
    X = ADnum(1, der =1)
    Y = ADmath.sin(X)+3
    labs = ADgraph.get_labels(Y)
    G = ADgraph.gen_graph(Y)
    cols = ADgraph.get_colors(G, Y)
    sizes = ADgraph.get_sizes(G, Y, labs)
    assert len(cols)== 4
    assert len(sizes) == 4

def test_draw_graph():
    X = ADnum(1, der =1)
    Y = ADmath.sin(X)+3
    fig = ADgraph.draw_graph(Y)
    assert type(fig) == matplotlib.figure.Figure

def test_gen_table():
    X = ADnum(1, der =1)
    Y = ADmath.sin(X)+3
    dat = ADgraph.gen_table(Y)
    assert type(dat) == pandas.core.frame.DataFrame
    

def test_plot_ADnum():
    X = ADnum(1, der =1)
    def Y(x):
        return ADmath.sin(x)
    fig = ADgraph.plot_ADnum(Y)
    assert type(fig)==matplotlib.figure.Figure
    
