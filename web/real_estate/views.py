from django.shortcuts import render
import folium
from django.views.generic import TemplateView
from django.core import serializers
from users.models import Properti, Training
import plotly.graph_objs as go
import plotly.io as pio
import json
import pandas as pd

predicted_class = 4
data_properti = serializers.serialize('json', Properti.objects.all())
data_training = serializers.serialize('json', Training.objects.all())
data_training = json.loads(data_training)
data_properti = json.loads(data_properti)
data_list = []
for i in range(len(data_training)):
    temp = data_training[i]["fields"]
    data_list.append(temp)
data_training = pd.DataFrame(data_list)
data_training["number"] = 1
donut_data = data_training[["label", "number"]].groupby("label", as_index=False).sum()

data_list_p = []
for i in range(len(data_properti)):
    temp = data_properti[i]["fields"]
    data_list_p.append(temp)
data_properti = pd.DataFrame(data_list_p)
data_properti['kecamatan'] = data_properti['kecamatan'].str.split(',').str[0]
data_properti = data_properti[data_properti.kecamatan != 'Sidoarjo']
data_properti["number"] = 1
# barchart_data = data_properti[data_properti["label"] == predicted_class]
barchart_data = data_properti[["kecamatan", "number"]].groupby("kecamatan", as_index=False).sum().head(7)

linechart_data = data_training[["tahun_dibangun", "harga"]].groupby("tahun_dibangun", as_index=False).mean()
linechart_data = linechart_data[linechart_data["tahun_dibangun"] >= 1500]

image_links = ["https://pic.rumah123.com/r123/720x420-crop/primary_property/project/1873/1661496821_63086df5912e0ads_images_1873.png", 
"https://picture.rumah123.com/r123-images/720x420-crop/customer/1969848/2024-05-20-03-39-01-96ac412e-d5e8-475b-82e2-062d15c336b4.jpg",
"https://picture.rumah123.com/r123-images/720x420-crop/customer/827735/2024-02-12-13-55-42-8eb594f9-6299-4ffc-b73d-f6061b4a6cb7.jpg"
]

def details(request):
    data = data_properti.drop(["judul", "link", "deskripsi",  "fasilitas", "last_update", "tipe_iklan", "id_iklan"], axis = 1)
    desc = data_properti["deskripsi"][1]
    row = data.to_dict('records')[0]
    context = {'data': row, 'desc' : desc}
    print("context", context)
    return render(request, 'details.html', context)

def index(request):
    return render(request, 'index.html')

def analyzer(request):
    return render(request, 'analyzer.html')

def result(request):
    return render(request, 'result.html')

class MapView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = data_properti[["judul", "kecamatan", "link"]].head(3)
        judul = data["judul"].tolist()
        kecamatan = data["kecamatan"].tolist()
        links = [link.strip("/").split("/")[-1] for link in data["link"].tolist()]
        print("links", links)
        context["data"] = zip(judul, kecamatan, links)
        
        # Create a map object
        m = folium.Map(location=[-7.2777318, 112.6470075], zoom_start=13, tiles='OpenStreetMap')
        
        # Add a Marker
        for lat, long in zip(data_training["latitude"].tolist(), data_training["longitude"].tolist()):
            folium.Marker(
                location=[lat, long],
                popup='Integration of Folium with Django',
                tooltip='Folium and Django',
            ).add_to(m)

        # Donut Chart
        # labels = ['Category A', 'Category B', 'Category C', 'Category D']
        # values = [4500, 2500, 1053, 500]
        # labels = donut_data["label"].tolist()
        # values = donut_data["number"].tolist()
        labels = ["Kelas 4", "Kelas Lain"]
        values = [4500, 5500]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=['orange', '#d3d3d3']))])
        fig.update_layout(
            annotations=[dict(text='Class', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        donut_chart_html = pio.to_html(fig, full_html=False)

        # Bar Chart
        # bar_x = ['Category A', 'Category B', 'Category C', 'Category D']
        # bar_y = [4500, 2500, 1053, 500]
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
        # line_x = ['January', 'February', 'March', 'April', 'May']
        # line_y = [10, 15, 13, 17, 18]
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