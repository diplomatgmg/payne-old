from django.views.generic import TemplateView

from mixins.views import TitleMixin
from ..shop.models import Product


# Create your views here.


class IndexView(TitleMixin, TemplateView):
    template_name = 'index/index.html'
    title = 'Главная'
    products = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['best_rating_product'] = self.products.order_by('rating').last()
        context['best_discount_product'] = self.products.order_by('-discount')[:3]
        context['newest_products'] = self.products.order_by('-added_at')[:8]
        context['bestselling_products'] = self.products.order_by('-count_sales')[:8]

        return context
