from .models import Cart

# function to show total cart items when user is loaded into the page,
# we should register those type of functions in settings.py in TEMPLATES
def cart_processor(request):
    if not request.session.session_key:
        request.session.create()

    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    return {
        'cart_total_items': cart.total_items,
        'cart_subtotal': cart.subtotal,
    }