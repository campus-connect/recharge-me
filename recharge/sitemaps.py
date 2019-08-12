#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib import sitemaps
from django.urls import reverse
from spirit.topic.models import Topic
from spirit.category.models import Category


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = "https"

    def items(self):
        return [
            'landing_page', 'about_page', 'contact_page'
        ]

    def location(self, item):
        return reverse(item)


class StaticAuthViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'Monthly'
    protocol = "https"

    def items(self):
        return [
            'account_signup', 'account_login',
        ]

    def location(self, item):
        return reverse(item)


class TopicSitemap(sitemaps.Sitemap):

    priority = 0.8
    protocol = "https"
    changefreq = 'daily'

    def items(self):
        return Topic.objects.visible()

    def lastmod(self, item):
        return item.last_active


class CategorySitemap(sitemaps.Sitemap):

    priority = 0.8
    protocol = "https"
    changefreq = 'Weekly'

    def items(self):
        return Category.objects.visible()

    def lastmod(self, item):
        return item.updated