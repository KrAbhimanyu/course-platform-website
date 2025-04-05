import os
import stripe
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

stripe.api_key = os.getenv("STRIPE_SECRET")

@router.post("/create-checkout-session")
def create_checkout_session(course_id: int):
    checkout = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 2000,
                'product_data': {'name': f'Course #{course_id}'},
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:3000/success',
        cancel_url='http://localhost:3000/cancel',
    )
    return JSONResponse({"checkout_url": checkout.url})