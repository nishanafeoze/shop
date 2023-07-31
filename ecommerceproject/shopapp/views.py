from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 6)

    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        products = paginator.page(1)

    return render(request, "category.html", {'category': c_page, 'products': products})

def proDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug, available=True)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    return render(request, "product.html", {'product': product})
