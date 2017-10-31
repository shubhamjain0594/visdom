# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from visdom import Visdom
import numpy as np
import math
import os.path
import getpass
from sys import platform as _platform
from six.moves import urllib

viz = Visdom()

assert viz.check_connection()

textwindow = viz.text('Hello World!')

updatetextwindow = viz.text('Hello World! More text should be here')
assert updatetextwindow is not None, 'Window was none'
viz.text('And here it is', win=updatetextwindow, append=True)

# video demo:
try:
    video = np.empty([256, 250, 250, 3], dtype=np.uint8)
    for n in range(256):
        video[n, :, :, :].fill(n)
    viz.video(tensor=video)

    # video demo: download video from http://media.w3.org/2010/05/sintel/trailer.ogv
    video_url = 'http://media.w3.org/2010/05/sintel/trailer.ogv'
    # linux
    if _platform == "linux" or _platform == "linux2":
        videofile = '/home/%s/trailer.ogv' % getpass.getuser()
    # MAC OS X
    elif _platform == "darwin":
        videofile = '/Users/%s/trailer.ogv' % getpass.getuser()
    # download video
    urllib.request.urlretrieve(video_url, videofile)

    if os.path.isfile(videofile):
        viz.video(videofile=videofile)
except ImportError:
    print('Skipped video example')


# image demo
viz.image(
    np.random.rand(3, 512, 256),
    opts=dict(title='Random!', caption='How random.'),
)

# grid of images
viz.images(
    np.random.randn(20, 3, 64, 64),
    opts=dict(title='Random images', caption='How random.')
)

# scatter plots
Y = np.random.rand(100)
viz.scatter(
    X=np.random.rand(100, 2),
    Y=(Y[Y > 0] + 1.5).astype(int),
    opts=dict(
        legend=['Apples', 'Pears'],
        xtickmin=-5,
        xtickmax=5,
        xtickstep=0.5,
        ytickmin=-5,
        ytickmax=5,
        ytickstep=0.5,
        markersymbol='cross-thin-open',
    ),
)

viz.scatter(
    X=np.random.rand(100, 3),
    Y=(Y + 1.5).astype(int),
    opts=dict(
        legend=['Men', 'Women'],
        markersize=5,
    )
)

# 2D scatterplot with custom intensities (red channel)
viz.scatter(
    X=np.random.rand(255, 2),
    Y=(np.random.rand(255) + 1.5).astype(int),
    opts=dict(
        markersize=10,
        markercolor=np.random.randint(0, 255, (2, 3,)),
    ),
)

# 2D scatter plot with custom colors per label:
viz.scatter(
    X=np.random.rand(255, 2),
    Y=(np.random.randn(255) > 0) + 1,
    opts=dict(
        markersize=10,
        markercolor=np.floor(np.random.random((2, 3)) * 255),
    ),
)

win = viz.scatter(
    X=np.random.rand(255, 2),
    opts=dict(
        markersize=10,
        markercolor=np.random.randint(0, 255, (255, 3,)),
    ),
)

# assert that the window exists
assert viz.win_exists(win)

# add new trace to scatter plot
viz.scatter(
    X=np.random.rand(255),
    Y=np.random.rand(255),
    win=win,
    name='new_trace',
    update='new'
)


# bar plots
viz.bar(X=np.random.rand(20))
viz.bar(
    X=np.abs(np.random.rand(5, 3)),
    opts=dict(
        stacked=True,
        legend=['Facebook', 'Google', 'Twitter'],
        rownames=['2012', '2013', '2014', '2015', '2016']
    )
)
viz.bar(
    X=np.random.rand(20, 3),
    opts=dict(
        stacked=False,
        legend=['The Netherlands', 'France', 'United States']
    )
)

# histogram
viz.histogram(X=np.random.rand(10000), opts=dict(numbins=20))

# heatmap
viz.heatmap(
    X=np.outer(np.arange(1, 6), np.arange(1, 11)),
    opts=dict(
        columnnames=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
        rownames=['y1', 'y2', 'y3', 'y4', 'y5'],
        colormap='Electric',
    )
)

# contour
x = np.tile(np.arange(1, 101), (100, 1))
y = x.transpose()
X = np.exp((((x - 50) ** 2) + ((y - 50) ** 2)) / -(20.0 ** 2))
viz.contour(X=X, opts=dict(colormap='Viridis'))

# surface
viz.surf(X=X, opts=dict(colormap='Hot'))

# line plots
viz.line(Y=np.random.rand(10), opts=dict(showlegend=True))

Y = np.linspace(-5, 5, 100)
viz.line(
    Y=np.column_stack((Y * Y, np.sqrt(Y + 5))),
    X=np.column_stack((Y, Y)),
    opts=dict(markers=False),
)

# line updates
win = viz.line(
    X=np.column_stack((np.arange(0, 10), np.arange(0, 10))),
    Y=np.column_stack((np.linspace(5, 10, 10), np.linspace(5, 10, 10) + 5)),
)
viz.line(
    X=np.column_stack((np.arange(10, 20), np.arange(10, 20))),
    Y=np.column_stack((np.linspace(5, 10, 10), np.linspace(5, 10, 10) + 5)),
    win=win,
    update='append'
)
viz.line(
    X=np.arange(21, 30),
    Y=np.arange(1, 10),
    win=win,
    name='2',
    update='append'
)
viz.line(
    X=np.arange(1, 10),
    Y=np.arange(11, 20),
    win=win,
    name='4',
    update='append'
)

Y = np.linspace(0, 4, 200)
win = viz.line(
    Y=np.column_stack((np.sqrt(Y), np.sqrt(Y) + 2)),
    X=np.column_stack((Y, Y)),
    opts=dict(
        fillarea=True,
        showlegend=False,
        width=400,
        height=400,
        xlabel='Time',
        ylabel='Volume',
        ytype='log',
        title='Stacked area plot',
        marginleft=30,
        marginright=30,
        marginbottom=80,
        margintop=30,
    ),
)

# boxplot
X = np.random.rand(100, 2)
X[:, 1] += 2
viz.boxplot(
    X=X,
    opts=dict(legend=['Men', 'Women'])
)

# stemplot
Y = np.linspace(0, 2 * math.pi, 70)
X = np.column_stack((np.sin(Y), np.cos(Y)))
viz.stem(
    X=X,
    Y=Y,
    opts=dict(legend=['Sine', 'Cosine'])
)

# quiver plot
X = np.arange(0, 2.1, .2)
Y = np.arange(0, 2.1, .2)
X = np.broadcast_to(np.expand_dims(X, axis=1), (len(X), len(X)))
Y = np.broadcast_to(np.expand_dims(Y, axis=0), (len(Y), len(Y)))
U = np.multiply(np.cos(X), Y)
V = np.multiply(np.sin(X), Y)
viz.quiver(
    X=U,
    Y=V,
    opts=dict(normalize=0.9),
)

# pie chart
X = np.asarray([19, 26, 55])
viz.pie(
    X=X,
    opts=dict(legend=['Residential', 'Non-Residential', 'Utility'])
)

# mesh plot
x = [0, 0, 1, 1, 0, 0, 1, 1]
y = [0, 1, 1, 0, 0, 1, 1, 0]
z = [0, 0, 0, 0, 1, 1, 1, 1]
X = np.c_[x, y, z]
i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
Y = np.c_[i, j, k]
viz.mesh(X=X, Y=Y, opts=dict(opacity=0.5))

# SVG plotting
svgstr = """
<svg height="300" width="300">
  <ellipse cx="80" cy="80" rx="50" ry="30"
   style="fill:red;stroke:purple;stroke-width:2" />
  Sorry, your browser does not support inline SVG.
</svg>
"""
viz.svg(
    svgstr=svgstr,
    opts=dict(title='Example of SVG Rendering')
)

# close text window:
viz.close(win=textwindow)

# assert that the closed window doesn't exist
assert not viz.win_exists(textwindow)

# Arbitrary visdom content
trace = dict(x=[1, 2, 3], y=[4, 5, 6], mode="markers+lines", type='custom',
             marker={'color': 'red', 'symbol': 104, 'size': "10"},
             text=["one", "two", "three"], name='1st Trace')
layout = dict(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})

viz._send({'data': [trace], 'layout': layout, 'win': 'mywin'})

# PyTorch tensor
try:
    import torch
    viz.line(Y=torch.Tensor([[0., 0.], [1., 1.]]))
except ImportError:
    print('Skipped PyTorch example')
