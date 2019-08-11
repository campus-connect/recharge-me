#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.views.generic.base import ContextMixin

class SeoMixin(ContextMixin):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CANONICAL_PATH'] = self.build_conical_link()
        return context

    def build_conical_link(self):
      return self.request.build_absolute_uri(self.request.path)