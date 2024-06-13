from django.shortcuts import render
import folium
from django.views.generic import TemplateView
from django.core import serializers
from users.models import Properti, Training
import plotly.graph_objs as go
import plotly.io as pio
import json
import pandas as pd

predicted_class = 6
data_training = serializers.serialize('json', Training.objects.all())
data_training = json.loads(data_training)
data_list = []
for i in range(len(data_training)):
    temp = data_training[i]["fields"]
    data_list.append(temp)
data_training = pd.DataFrame(data_list)
data_training["number"] = 1
donut_data = data_training[["label", "number"]].groupby("label", as_index=False).sum()
data_clustered = data_training[data_training["label"] == predicted_class]
barchart_data = data_clustered[["kecamatan_1", "number"]].rename({"kecamatan_1" : "kecamatan"}, axis = 1).groupby("kecamatan", as_index=False).sum().head(7)
linechart_data = data_clustered[["tahun_dibangun", "harga"]].groupby("tahun_dibangun", as_index=False).mean()
linechart_data = linechart_data[linechart_data["tahun_dibangun"] >= 1500]

def details(request):
    # data = data_training.drop(["judul", "link", "deskripsi",  "fasilitas", "last_update", "tipe_iklan", "id_iklan"], axis = 1)
    # desc = data_training["deskripsi"][1]
    # row = data.to_dict('records')[0]
    # context = {'data': row, 'desc' : desc}
    # print("context", context)
    # return render(request, 'details.html', context)
    return render(request, 'details.html')

def index(request):
    data = data_training[["judul", "images_link"]].head(3)
    judul = data["judul"].tolist()
    image = data["images_link"].tolist()
    context = {"data" : zip(judul, image)}
    return render(request, 'index.html', context)

def analyzer(request):
    context = {}
    cols = ["kecamatan_1", "sertifikat", "sumber_air", "kondisi_perabotan", "kondisi_properti", "pemandangan"]
    for col in cols:
        context[col] = data_training[col].unique().tolist()
    return render(request, 'analyzer.html', context)

def result(request):
    return render(request, 'result.html')

class MapView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = data_training[["judul", "kecamatan_1", "link"]].rename({"kecamatan_1" : "kecamatan"}, axis = 1).head(3)
        judul = data["judul"].tolist()
        kecamatan = data["kecamatan"].tolist()
        links = [link.strip("/").split("/")[-1] for link in data["link"].tolist()]
        print("links", links)
        context["data"] = zip(judul, kecamatan, links)
        
        # Create a map object
        m = folium.Map(location=[-7.2777318, 112.6470075], zoom_start=13, tiles='OpenStreetMap')
        
        # Add a Marker
        for lat, long, judul in zip(data_clustered["latitude"].tolist(), data_clustered["longitude"].tolist(), data_clustered["judul"].tolist()):
            folium.Marker(
                location=[lat, long],
                popup='Integration of Folium with Django',
                tooltip=judul,
            ).add_to(m)

        # Donut Chart
        labels = [f"Kelas {predicted_class}", "Kelas Lain"]
        values = [donut_data[donut_data["label"] == predicted_class]["number"].sum(), donut_data[donut_data["label"] != predicted_class]["number"].sum()]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=['orange', '#d3d3d3']))])
        fig.update_layout(
            annotations=[dict(text='Class', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        donut_chart_html = pio.to_html(fig, full_html=False)

        # Bar Chart
        bar_x = barchart_data["kecamatan"].tolist()
        bar_y = barchart_data["number"].tolist()
        bar_fig = go.Figure(data=[go.Bar(x=bar_x, y=bar_y, marker=dict(color='orange'))])
        bar_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis=dict(gridcolor='#d3d3d3')
        )
        bar_chart_html = pio.to_html(bar_fig, full_html=False)

        # Line Chart
        line_x = linechart_data["tahun_dibangun"].tolist()
        line_y = linechart_data["harga"].tolist()
        line_fig = go.Figure(data=[go.Scatter(x=line_x, y=line_y, mode='lines+markers', line=dict(color='orange'))])
        line_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(gridcolor='#d3d3d3'),
            yaxis=dict(gridcolor='#d3d3d3')
        )
        line_chart_html = pio.to_html(line_fig, full_html=False)
        
        # Render the chart
        context['map'] = m._repr_html_()
        context['donut_chart'] = donut_chart_html
        context['bar_chart'] = bar_chart_html
        context['line_chart'] = line_chart_html
        return context