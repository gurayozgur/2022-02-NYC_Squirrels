import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

def plot_maps(nyc_squirrels, plotted_feature = "all", save_fig=False):

  BBox = (nyc_squirrels.long.min(), nyc_squirrels.long.max(), nyc_squirrels.lat.min(), nyc_squirrels.lat.max())

  fig, ax = plt.subplots(figsize = (10,8.75))
  ax.set_xlim(BBox[0],BBox[1])
  ax.set_ylim(BBox[2],BBox[3])
  ax.set_xticks([])
  ax.set_yticks([])

  if plotted_feature != "all":
    counts = pd.DataFrame(nyc_squirrels[plotted_feature].value_counts()).reset_index()
    i = 0
    for x in counts["index"]:
      nyc_squirrels_plotted_feature = nyc_squirrels[nyc_squirrels[plotted_feature]==x]
      ax.scatter(nyc_squirrels_plotted_feature.long, nyc_squirrels_plotted_feature.lat, zorder=1, alpha=0.3, c=cm.hsv(float(i) / len(counts["index"])), s=10)
      i = i + 1
    if plotted_feature != "hectare":
      plt.legend(counts["index"])

  else:
    ax.scatter(nyc_squirrels.long, nyc_squirrels.lat, zorder=1, alpha=0.3, c="black", s=10)

  ax.imshow(plt.imread("fig/map.png"), zorder=0, extent = BBox, aspect=None)
  plt.title(plotted_feature)  

  if save_fig:
    plt.savefig("fig/map_"+str(plotted_feature)+".pdf",bbox_inches="tight")

def plot_counts(nyc_squirrels, plotted_feature = "all", save_fig=False):
  if plotted_feature != "all":
    counts = pd.DataFrame(nyc_squirrels[plotted_feature].value_counts()).reset_index()
    fig, ax = plt.subplots()
    ax.bar(counts["index"], counts[plotted_feature])
    plt.xticks(counts["index"],rotation=75)
    plt.yticks()
    plt.xlabel(plotted_feature)
    plt.ylabel("counts")
    return dict(zip(counts["index"],counts[plotted_feature]))
  else:
    print("Number of observations is "+str(nyc_squirrels.shape[0])+".")
    return nyc_squirrels.shape[0]

  if save_fig:
    plt.savefig("fig/count_"+str(plotted_feature)+".pdf",bbox_inches="tight") 

def heatmap(nyc_squirrels, save_fig=False):
  squirrels_hectare = pd.DataFrame(nyc_squirrels["hectare"].value_counts()).reset_index()
  squirrels_hectare.columns = ["hectare", "number"]
  hectare_code1 = []
  hectare_code2 = []
  for x in squirrels_hectare["hectare"].tolist():
      hectare_code1.append(x[0]+x[1])
      hectare_code2.append(x[2])
  squirrels_hectare["hectare_code1"] = hectare_code1
  squirrels_hectare["hectare_code2"] = hectare_code2

  keys = squirrels_hectare.sort_values("hectare")["hectare"]
  values = squirrels_hectare.sort_values("hectare")["number"]
  dictionary = dict(zip(keys, values))

  def f(sum_list, dictionary):
      Z = []
      for i in sum_list:
          for j in i.tolist():
              if j in dictionary:
                  Z.append(dictionary[j])
              else:
                  Z.append(0)
      return Z

  x = squirrels_hectare.sort_values("hectare_code1")["hectare_code1"].unique()
  y = squirrels_hectare.sort_values("hectare_code2")["hectare_code2"].unique()
  X, Y = np.meshgrid(x, y)

  sum_list = [a + b for a, b in zip(X, Y)]
  Z = f(sum_list, dictionary)

  x = np.linspace(1, 42, 42)
  y = np.linspace(1, 10, 9)
  X, Y = np.meshgrid(x, y)
  Z = np.array(Z).reshape(X.shape)

  fig, ax = plt.subplots(figsize = (14,5))
  plt.xticks(x)
  plt.yticks(y)
  from matplotlib.ticker import NullFormatter
  ax.xaxis.set_major_formatter(NullFormatter())
  ax.yaxis.set_major_formatter(NullFormatter())
  plt.contourf(X, Y, Z, 20, cmap='viridis')
  plt.colorbar()

  if save_fig:
    plt.savefig("fig/heatmap.pdf",bbox_inches="tight")

def plot_correlation(nyc_squirrels, labels, name, save_fig=False):

  fig, ax = plt.subplots(1,1, figsize=(8, 8))
  im = ax.imshow(nyc_squirrels[labels].corr())
  ax.set_xticks(range(len(labels)))
  ax.set_yticks(range(len(labels)))
  ax.set_xticklabels(labels, rotation=90)
  ax.set_yticklabels(labels, rotation=0)
  plt.colorbar(im, ax=ax)
  plt.show()

  if save_fig:
    plt.savefig("fig/"+name+".pdf",bbox_inches="tight")


def dict_plot(D, count, name, save_fig=False):

  plt.bar(range(len(D)), list(D.values()), align='center')
  plt.bar(range(len(count)), list(count.values()), color="orange", align='center')
  plt.xticks(range(len(D)), list(D.keys()), rotation=90)
  plt.title("Prediction Accuracy")
  plt.show()
  if save_fig:
    plt.savefig("fig/"+name+".pdf",bbox_inches="tight")

    