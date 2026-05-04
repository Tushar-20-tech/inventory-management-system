"""
URL configuration for inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from main.views import home, reports_view ,signup_view ,login_view, stock_out_view
from django.conf import settings
from django.conf.urls.static import static
from main.views import dashboard,profile_view, delete_account,products_view,add_product,delete_product,edit_product ,stock_in_view,how_to_use_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('delete-account/', delete_account, name='delete_account'),
    path("products/", products_view, name="products"),

    path("add-product/", add_product, name="add_product"),
    path("delete-product/<int:product_id>/",delete_product,name="delete_product"),
    path("edit-product/<int:product_id>/",edit_product,name="edit_product"),
    path("stock-in/", stock_in_view, name="stock_in"),
    path("stock-out/", stock_out_view, name="stock_out"),
    path("reports/", reports_view, name="reports"),
    path("how-to-use/", how_to_use_view, name="how_to_use"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
