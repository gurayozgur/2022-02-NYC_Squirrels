import numpy as np
import pandas as pd

def dataset_fix(nyc_squirrels):
  
  nyc_squirrels = nyc_squirrels.drop(columns=['unique_squirrel_id', 
       'hectare_squirrel_number', 
       'combination_of_primary_and_highlight_color', 'color_notes', 'location', 
       'specific_location', "above_ground_sighter_measurement",
       'other_interactions', 'lat_long', 'zip_codes', 'community_districts',
       'borough_boundaries', 'city_council_districts', 'police_precincts'], axis=1)
  
  nyc_squirrels["date"]= pd.to_datetime(nyc_squirrels["date"],format='%m%d%Y')
  nyc_squirrels["age"] = nyc_squirrels["age"].fillna("Unknown")
  nyc_squirrels["age"] = nyc_squirrels["age"].replace("?", "Unknown")
  nyc_squirrels["other_activities"] = nyc_squirrels["other_activities"].replace("unknown", np.nan)
  nyc_squirrels["other_activities"] = nyc_squirrels["other_activities"].fillna(0)

  return nyc_squirrels

def numColor(color):
  if(not isinstance(color, str)):
    return 0
  else:
    num = color.count(',') + 1
    return num

def dataset_numerate(nyc_squirrels):
  nyc_squirrels = nyc_squirrels.drop(columns=['hectare', 'date', 'other_activities'], axis=1)
  
  nyc_squirrels["slot"] = nyc_squirrels["slot"].replace("AM", 0.0)
  nyc_squirrels["slot"] = nyc_squirrels["slot"].replace("PM", 1.0)
  nyc_squirrels["age"] = nyc_squirrels["age"].replace("Adult", 1.0)
  nyc_squirrels["age"] = nyc_squirrels["age"].replace("Juvenile", 0.0)
  nyc_squirrels["age"] = nyc_squirrels["age"].replace("Unknown", 0.5)
  nyc_squirrels["primary_fur_color"] = nyc_squirrels["primary_fur_color"].fillna("Unknown")
  nyc_squirrels["highlight_fur_color"] = nyc_squirrels["highlight_fur_color"].fillna("Unknown")
  for x in nyc_squirrels.primary_fur_color.unique():
    nyc_squirrels.loc[(nyc_squirrels.primary_fur_color == x), "primary_" + x]=1
  for x in nyc_squirrels.primary_fur_color.unique():
    nyc_squirrels["primary_" + x] = nyc_squirrels["primary_" + x].fillna(0)
  for x in nyc_squirrels.highlight_fur_color.unique():
    nyc_squirrels.loc[(nyc_squirrels.highlight_fur_color == x), "highlight_" + x]=1
  for x in nyc_squirrels.highlight_fur_color.unique():
    nyc_squirrels["highlight_" + x] = nyc_squirrels["highlight_" + x].fillna(0)
  nyc_squirrels = nyc_squirrels.replace(False, 0)
  nyc_squirrels = nyc_squirrels.replace(True, 1)
  nyc_squirrels = nyc_squirrels.drop(columns=['primary_fur_color', 'highlight_fur_color'], axis=1)
  return nyc_squirrels
