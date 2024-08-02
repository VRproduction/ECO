from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.AboutPageView.as_view(), name = 'about'),
    path('shop/', views.ShopPageView.as_view(), name = 'shop'),
    path('companies/', views.CompanyPageView.as_view(), name = 'companies'),
    path('contact/', views.ContactPageView.as_view(), name = 'contact'),
    path('account/', views.AccountPageView.as_view(), name = 'account'),

    path('products/<slug:slug>/', views.ProductDetailPageView.as_view(), name = 'product-detail'),

    path('blogs/', views.BlogPageView.as_view(), name = 'blog'),
    path('blogs/<slug:slug>/', views.BlogDetailPageView.as_view(), name='blog-detail'),

    # path('vacancies/', views.VacanciesPageView.as_view(), name = 'vacancies'),

    path('basket/', views.BasketPageView.as_view(), name = 'basket'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('remove-from-basket/<int:basket_item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('get-basket-items/', views.get_basket_items, name='get_basket_items'),
    path('update_basket_item_count/<int:product_id>/', views.update_basket_item_count, name='update_basket_item_count'),
    path('clear-basket/', views.clear_basket, name='clear_basket'),
    path('delete_selected_basket_items/', views.delete_selected_basket_items, name='delete_selected_basket_items'),
    path('checkout/', views.checkout, name='checkout'),
    path('check-stock-status/', views.check_stock_api, name='check_stock'),

    path('wish-list/', views.WishListPageView.as_view(), name='wish_list'),
    path('favorite_toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite_api'),

    path('start-task/', views.start_task, name='start_task'),

]