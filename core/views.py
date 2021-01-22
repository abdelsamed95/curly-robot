from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from .models import Item, ItemImage, OrderItem, Order, Home


def contact(request):
    """
    docstring
    """
    return render(request, "contact.html")


def HomeView(request):
    home = Home.objects.all()
    return render(request, 'home.html', {'home': home})


def ItemDetailView(request, slug):
    item = get_object_or_404(Item, slug=slug)
    photos = ItemImage.objects.filter(item=item)
    return render(request, 'product.html', {
        'object': item,
        'photos': photos
    })


class ItemsView(ListView):
    model = Item
    template_name = "products.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, message="this item quantity was updated.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, message="this item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request, message="this item was added to your cart.")
        return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(
                request, message="this item was removed from your cart.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, message="this item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, message="you do not have an acive order")
        return redirect("core:product", slug=slug)
