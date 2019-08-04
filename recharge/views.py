#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.views.generic.base import TemplateView

class LandingView(TemplateView):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'landing'
        context["title"] = 'Home'
        return context
    

class AboutView(TemplateView):
    template_name = "landing/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'about'
        context["title"] = 'About Us'
        return context

class ContactView(TemplateView):
    template_name = "landing/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'contact'
        context["title"] = 'Contact Us'
        return context
    