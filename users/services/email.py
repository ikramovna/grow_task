import random
from templated_mail.mail import BaseEmailMessage
from apps.users.services.cache_functions import setKey


class ActivationEmail(BaseEmailMessage):
    template_name = "activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activation_code'] = random.randint(100000, 999999)

        setKey(
            key=context.get('email'),

            value=context.get('activation_code'),
            timeout=None
        )
        return context
