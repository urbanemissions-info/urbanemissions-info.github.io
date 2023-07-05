import pandas as pd
from pathlib import Path
import os
import pygal

path = str(Path(os.getcwd()))

source_apportionment_df = pd.read_csv(path+"/source_apportionment/data/APnA_50airsheds_PM25_Source_Apportionment_CAMxOutputs.csv")
source_apportionment_df = source_apportionment_df.fillna('0%')

data = pd.melt(source_apportionment_df, id_vars=['City', 'study_year'], value_vars=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
sources_dict = {'A':'Transport',
                'B': 'Residential',
                'C': 'Industries',
                'D': 'All dust',
                'E': 'Open waste burning',
                'F': 'Diesel generator sets',
                'G': 'Brick manufacturing',
                'H': 'Sea Salt',
                'I': 'Outside/Regional contribution'}

for city in data.City.unique():
    city_data = data[data.City==city]
    city_data = city_data.replace({'variable':sources_dict})
    study_year = city_data.study_year.unique()[0]
    pie_chart = pygal.Pie(truncate_legend=100, legend_at_bottom=True, legend_at_bottom_columns=3)
    pie_chart.title = "Source Apportionment {} - {}".format(city, study_year)
    for idx, row in city_data.iterrows():
        label = row['variable']
        data_points = float(row['value'][:-1])
        pie_chart.add(label, data_points)

    pie_chart.render_to_file(path+'/source_apportionment/plots/{}_source_apportionment_pie.svg'.format(city))
