import re

from django.views.generic import ListView, DetailView

from mixins.views import TitleMixin
from .models import Product


class ShopView(TitleMixin, ListView):
    model = Product
    template_name = 'shop/shop.html'
    title = 'Магазин'
    paginate_by = 8
    paginate_orphans = 4

    def get_ordering(self):  # сохранение фильтрации при поиске товара
        request = self.request
        if not request.GET.get('ordering'):
            pattern = r'ordering=.\w+'
            referer = request.META.get('HTTP_REFERER')
            search = re.search(pattern, referer)
            if search:
                return search.group().split('=')[1]
        return request.GET.get('ordering', '-rating')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['ordering'] = self.get_ordering()
        context['search'] = self.request.GET.get('search', '')

        return context

    def get_queryset(self):
        search = ' '.join(self.request.GET.get('search', '').lower().split())
        object_list = self.model.objects.order_by(self.get_ordering())
        if search:
            object_list = [obj for obj in object_list if search in str(obj).lower()]
        return object_list


class ShopProductView(DetailView):
    model = Product
    template_name = 'shop/product_details.html'
