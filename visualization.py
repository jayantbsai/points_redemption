import random
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series
from matplotlib.backend_bases import MouseEvent

# load data from csv
df = pd.read_csv('files/data.csv')

# get list of unique product types
types = df['type'].unique()

# create a color mapping for each type of product
rand_colors = ["#"+''.join([random.choice('0123456789ABCDEF')
               for j in range(6)])
               for i in range(len(types))]

# create a color lookup based on type
color_lookup = { types[i]: rand_colors[i] for i in range(0, len(types)) }

# graphing
x = df['type']
y = df['value'] = df['price']/df['points']
c = df['color'] = [color_lookup[t] for t in x]
df = df.sort_values('value')

# create subplot
fig, ax = plt.subplots()

# scatter plot
sc = ax.scatter(x, y, color=c)

# setup annotation
bbox_dict = { 'facecolor': 'white',
              'edgecolor': 'lightgray',
              'boxstyle': 'round' }
annot = ax.annotate('',
                    xy=(0,0),
                    xytext=(0,20),
                    xycoords='data',
                    textcoords='offset pixels',
                    ha='center',
                    va='bottom',
                    bbox={**bbox_dict})
annot.set_visible(False)

def get_tooltip(indices: []) -> str:
    """
    generate tooltip string for all indices in mouse event. tooltips are shown
    in descending value order. this is to match how they are displayed in the
    graph
    """
    # get all the rows based on indices, then sort
    rows = df.loc[indices].sort_values(by='value', ascending=False)
    # iterate thru' each row and get tooltip
    return '\n'.join([fmt_tooltip(row) for index, row in rows.iterrows()])

def fmt_tooltip(row: Series) -> str:
    """
    format tooltip string by joining all tooltips
    """
    # set max characters to trim tooltip at
    trim_max = 40
    # format tooltip string, then trim
    tooltip = f"{round(row['value'], 4)}: {row['product']}"
    return tooltip if len(tooltip) < 40 else f"{tooltip[:trim_max-3]}..."

def hover(event: MouseEvent):
    """
    handle mouse move
    """
    # Checks if scatter plot contains mouseevet
    cont, det = sc.contains(event)

    # if contained, show tooltip
    if cont:
        annot.xy = (event.xdata, event.ydata)
        annot.set_text(get_tooltip(det['ind']))
        annot.set_visible(True)
    else:
        annot.set_visible(False)
        annot.set_text('')

    # force redraw
    event.canvas.draw()

# attach mouse handler
fig.canvas.mpl_connect('motion_notify_event', hover)

# config graph & show
plt.xticks(rotation=90)
plt.show()
