from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, ListView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm, CouponForm
from .models import Item, Order, OrderItem, Coupon, BillingAddress, Payment
from userpanel.models import Business, User
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.


class ItemDetailView(DetailView):
    model = Item
    template_name = 'ecommerce/product-page.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ['title', 'price', 'discounted_price',
              'category', 'label', 'desciption', 'image_1', 'image_2', 'image_3']
    template_name = 'ecommerce/item_create_form.html'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.business = self.request.user
        item.save()
        # final_item = FinalItem.objects.create(
        #     business_user=self.request.user, items=item)
        messages.success(
            self.request, 'The Item was created with success! Go ahead and add some more now.')
        return redirect('businesses:business-dashboard')


class BusinessItemListView(ListView):
    model = Item
    template_name = 'business/business_item_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'items'
    # paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(business=user)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "ecommerce/order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                'order': order,
                "couponform": CouponForm(),
                "DISPLAY_COUPON_FORM": True,
            }
            return render(self.request, 'ecommerce/checkout-page.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("ecommerce:checkout_list")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get(
                    'apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_shipping_address = form.cleaned_data.get(
                #     'same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == 'S':
                    return redirect('ecommerce:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('ecommerce:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, 'Invalid payment option selected')
                    return redirect('ecommerce:checkout_list')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("ecommerce:order-summary")


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated!")
            return redirect("ecommerce:order-summary")
        else:
            order.item.add(order_item)
            messages.info(request, "Your item has been Added to your cart!")
            return redirect("ecommerce:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, "This item has been Added to your cart!")
        return redirect("ecommerce:order-summary")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            messages.info(request, "This item was removed to your cart!")
            return redirect("ecommerce:order-summary")
        else:
            messages.info(request, "This item is not in your cart!")
            return redirect("ecommerce:product_list", pk=pk)
    else:
        messages.info(request, "sorry, You don't have any order!")
        return redirect("ecommerce:product_list", pk=pk)


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            messages.info(request, "This item was quantity was updated!")
            return redirect("ecommerce:order-summary")
        else:
            messages.info(request, "This item is not in your cart!")
            return redirect("ecommerce:product_list", pk=pk)
    else:
        messages.info(request, "sorry, You don't have any order!")
        return redirect("ecommerce:product_list", pk=pk)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("ecommerce:checkout_list")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("ecommerce:checkout_list")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("ecommerce:checkout_list")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                "order": order,
                "DISPLAY_COUPON_FORM": False,
            }
            return render(self.request, "ecommerce/payment.html", context)
        else:
            messages.warning(
                self.request, "Please first add the billing address")
            return redirect("core:checkout_list")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)  # cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )
            # create the payment

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order_item = order.items.all()
            order_item.update(ordered=True)
            for item in order_item:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not Authentication")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "something went wrong. You were not charged, try again!!")
            return redirect("/")

        except Exception as e:
            #  send a email to ourselves
            messages.warning(
                self.request, "A serious error occured.we have been notified!")
            return redirect("/")
