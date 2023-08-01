from cart.models import Cart
from wishlist.models import Wishlist

def cart_and_wishlist_counts(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        cart=Cart.objects.filter(user=request.user)

        total_price=0
        for item in cart:
            product_price = item.product.product_price
            product_offer = item.product.offer
            brand_offer = item.product.brand.offer

            if product_offer is None and brand_offer is None:
                total_price += product_price * item.product_qty
            
            
            else:
                if product_offer and brand_offer:
                    # If both product and brand have offers, choose the maximum discount
                    max_discount = max(product_offer.discount_amount, brand_offer.discount_amount)
                elif product_offer:
                    max_discount = product_offer.discount_amount
                else:
                    max_discount = brand_offer.discount_amount

                discount = (max_discount / 100) * product_price
            
                discounted_price = product_price - discount

                total_price += discounted_price * item.product_qty
            
           

        

    else:
        cart_count=0
        wishlist_count=0
        cart=0
        total_price=0
        


    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'cart':cart,
        'total_price':total_price
    }