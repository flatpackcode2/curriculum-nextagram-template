import braintree
import os

gateway= braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('BT_MERCHANT'),
        public_key=os.getenv('BT_PUBLIC'),
        private_key=os.getenv('BT_PRIVATE')
    )
)
