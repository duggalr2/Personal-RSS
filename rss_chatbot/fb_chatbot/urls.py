from django.conf.urls import include, url
from .views import Rss_view

urlpatterns = [
    url(r'^b102666bd0971ac426a28b51b421f9a982880718b1ce10e5bf/?$', Rss_view.as_view())
]
