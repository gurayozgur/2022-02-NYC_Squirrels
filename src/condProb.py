import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def behaviourUpdate(frame,object,keyword):
  #Reads out all behaviours for a given squirrel and adds them to a dataframe under the keyword
  for column in frame.columns:
    if(object[column]):
      frame[column][keyword] += 1

def update(frame, object, keyword):
  #Checks for keyword presence then reads behaviour
  if(object[keyword]):
    behaviourUpdate(frame, object, keyword)

def plot_behaviourmap(nyc_squirrels, behaviours, behaviour_relation, save_fig=False):

  for index, row in behaviours.iterrows():
    for column in behaviour_relation.columns:
      update(behaviour_relation, row, column)

  for row in behaviour_relation.index:
    ref_val = behaviour_relation[row][row]
    for col in behaviour_relation.columns:
      behaviour_relation[col][row] = round((behaviour_relation[col][row]/ref_val)*100, 1)

  fig, ax = plt.subplots(1,1, figsize=(8, 8))
  ax.imshow(behaviour_relation)
  ax.set_xticks(range(len(behaviour_relation.index)))
  ax.set_yticks(range(len(behaviour_relation.index)))
  ax.set_xticklabels(behaviour_relation.columns, rotation=90)
  ax.set_yticklabels(behaviour_relation.columns, rotation=0)

  # Rotate the tick labels and set their alignment.
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
          rotation_mode="anchor")

  # Loop over data dimensions and create text annotations.
  for i in range(len(behaviour_relation.index)):
      for j in range(len(behaviour_relation.index)):
          text = ax.text(j, i, behaviour_relation.iloc[i, j],
                        ha="center", va="center", color="w", fontsize="x-small")
  if save_fig:
    fig.savefig('fig/BehaviourHeatmap.pdf', bbox_inches='tight', dpi=500)