from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

try:
    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail.core import urls as wagtail_urls
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailadmin import urls as wagtailadmin_urls
    from wagtail.wagtailcore import urls as wagtail_urls

from experiments import views as experiment_views


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^experiments/complete/([^\/]+)/$', experiment_views.record_completion),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(wagtail_urls)),
]
