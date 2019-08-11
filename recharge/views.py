#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.views.generic.base import TemplateView
from accounts.mixin import SeoMixin

class LandingView(TemplateView, SeoMixin):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'landing'
        context["title"] = 'Unlimited Peer-to-peer airtime and data funding'
        return context
    

class AboutView(TemplateView, SeoMixin):
    template_name = "landing/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'about'
        context["title"] = 'About Us'
        return context

class ContactView(TemplateView, SeoMixin):
    template_name = "landing/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'contact'
        context["title"] = 'Contact Us'
        return context
    