from django.conf.urls import url
 
from . import view
from TestModel import views as model_view
 
urlpatterns = [
    url(r'^hello$', view.hello),
    url(r'^index$', model_view.index),
    url(r'^base$', model_view.base),
    url(r'^get_top$',model_view.get_top),
    url(r'^get_allpath$',model_view.get_allpath),
    url(r'^get_newslist$',model_view.get_newslist),
    url(r'^demo$',model_view.demo),
    url(r'^get_demo$',model_view.get_demo),
]