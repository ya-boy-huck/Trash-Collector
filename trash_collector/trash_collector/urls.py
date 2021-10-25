"""trash_collector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # First adding our custom routes from our accounts app's urls.py (for our custom registration)
    path('accounts/', include('accounts.urls')),
    # Then adding Django's built in routes (login and logout). Notice there is no 'login' function in accounts/views.py. Django takes care of this for us.
    path('accounts/', include('django.contrib.auth.urls')),
    # Adding all urls from customer app
    path('customers/', include('customers.urls')),
    # Adding all urls from employees app
    path('employees/', include('employees.urls')),
    # 'home' redirects a user to the appropriate index based on their auth group. Investigate trach_collector/views.py for more info
    path('', views.group_redirect, name='home')
]
