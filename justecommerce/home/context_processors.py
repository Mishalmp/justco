from cart.models import Cart
from wishlist.models import Wishlist

def cart_and_wishlist_counts(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }