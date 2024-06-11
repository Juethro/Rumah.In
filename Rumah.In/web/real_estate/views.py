from django.shortcuts import render
import folium
from django.views.generic import TemplateView
from .utils import make_markers_and_add_to_map
import plotly.graph_objs as go
import plotly.io as pio

def details(request):
    return render(request, 'details.html')

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
        
        # Create a map object
        m = folium.Map(location=[40.416, -3.70], zoom_start=11, tiles='OpenStreetMap')
        
        # Add a Marker
        folium.Marker(
            location=[40.417, -3.70],
            popup='Integration of Folium with Django',
            tooltip='Folium and Django',
        ).add_to(m)

        # Donut Chart
        labels = ['Category A', 'Category B', 'Category C', 'Category D']
        values = [4500, 2500, 1053, 500]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
        fig.update_layout(
            annotations=[dict(text='Categories', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        donut_chart_html = pio.to_html(fig, full_html=False)

        # Bar Chart
        bar_x = ['Category A', 'Category B', 'Category C', 'Category D']
        bar_y = [4500, 2500, 1053, 500]
        bar_fig = go.Figure(data=[go.Bar(x=bar_x, y=bar_y)])
        bar_chart_html = pio.to_html(bar_fig, full_html=False)

        # Line Chart
        line_x = ['January', 'February', 'March', 'April', 'May']
        line_y = [10, 15, 13, 17, 18]
        line_fig = go.Figure(data=[go.Scatter(x=line_x, y=line_y, mode='lines+markers')])
        line_chart_html = pio.to_html(line_fig, full_html=False)
        
        # Render the map to HTML
        context['map'] = m._repr_html_()
        context['donut_chart'] = donut_chart_html
        context['bar_chart'] = bar_chart_html
        context['line_chart'] = line_chart_html
        return context