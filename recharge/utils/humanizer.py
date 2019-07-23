#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

def humanize_list(elements):
    """"
    splits a list and add punctuations to it elements
    """
    humanize_string = ''
    for element in elements:
        if element == elements[len(elements)-2]: #second to last item
            humanize_string = humanize_string + element.username+' and '
        elif element == elements[len(elements)-1]: # last item
            humanize_string = humanize_string + element.username
        else:
            humanize_string = humanize_string + element.username+', '
    return humanize_string