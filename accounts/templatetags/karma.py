#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import template

register = template.Library()

@register.inclusion_tag('tags/karma.html', takes_context=True)
def karma(context):
    
    request = context.get('request', None)
    if request:
        user = request.user
        if user.is_authenticated:
            return {
                'karma': (user.karma / 10) * 100,
                'point': user.karma
            }
    
