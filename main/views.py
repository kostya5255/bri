from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, Product
import json

#Коммитим не палимся
def catalogue(request):
    products = Product.objects.all()
    return render(request, "main/catalogue.html", {"products": products})


def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


def order(request):
    return render(request, "main/order.html")


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session["cart"] = cart

    return redirect("main:catalogue")


def cart(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total += subtotal
        cart_items.append(
            {"product": product, "quantity": quantity, "subtotal": subtotal}
        )

    return render(request, "main/cart.html", {"cart_items": cart_items, "total": total})


def update_cart(request, product_id):
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1

        cart = request.session.get("cart", {})

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)  # Remove if 0 or less

        request.session["cart"] = cart

    return redirect("main:cart")


def checkout(request):
    # Step 1: Get the cart data from the session
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("main:catalogue")  # Redirect if the cart is empty

    # Step 2: Get the products from the database that are in the cart
    products = Product.objects.filter(id__in=cart.keys())

    # Step 3: Prepare cart items and calculate the total
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total += subtotal
        cart_items.append(
            {"product": product, "quantity": quantity, "subtotal": subtotal}
        )

    # Step 4: Process form submission if it's a POST request
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order
            order = form.save(commit=False)

            # Save the cart data as a JSON string with just product names and quantities
            readable_cart = []
            for item in cart_items:
                readable_cart.append(
                    {
                        "name": item["product"].name,
                        "quantity": item["quantity"],
                    }
                )

            order.cart_data = json.dumps(readable_cart, ensure_ascii=False)
            order.total_price = total
            order.save()  # Save the order

            # Clear the cart after successful order placement
            request.session["cart"] = {}

            # Redirect to the order success page with the order ID
            return redirect("main:order_success", order_id=order.id)

    else:
        form = OrderForm()  # GET request, just display the form

    # Step 5: Render the checkout page with cart data
    return render(
        request,
        "main/checkout.html",
        {"form": form, "cart_items": cart_items, "total": total},
    )


def order_success(request, order_id):
    # Get the order from the database
    order = get_object_or_404(Order, id=order_id)

    # Parse the cart data (which is stored as JSON)
    cart_items = json.loads(order.cart_data)

    # Calculate the total price dynamically
    total = 0
    for item in cart_items:
        product = Product.objects.get(name=item["name"])  # Get the product by name
        subtotal = item["quantity"] * product.price
        item["subtotal"] = subtotal
        total += subtotal

    return render(
        request,
        "main/order_success.html",
        {"order": order, "cart_items": cart_items, "total": total},
    )
