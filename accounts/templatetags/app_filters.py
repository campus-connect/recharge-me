#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import template

register = template.Library()

@register.filter(name='task_filter')
def task_filter(task):
    if task == 'S':
        return 'Send Funding'
    elif task == 'R':
        return 'Receive Funding'
    else:
        return '--'