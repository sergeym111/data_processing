import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'sergeym1111'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1642688764:AetQAJBafTO+umUa990m18Rd7sKqIilxsIcswpq0LJLDKjomsnl96rMA/uuomxdsbRTkXaMow7Mu4pzPeqan2cYcHTUEhSqxbNgvVDjR3CEIh+dgnxVIgzgCqr6QlMmEIQ13CuMF1QBX/5SGC9Cs'
    # user = 'ai_machine_learning'
    # users = ['vfanc.ru', 'remont_kholodilnikov_stiralok']
    users = ['vfanc.ru']
    # insta_graf_ql_link = 'https://www.instagram.com/graphql/query/?'
    insta_followers_link = 'https://i.instagram.com/api/v1/friendships/'
    # posts_query_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'X-CSRFToken': csrf,
                                          'User-Agent': 'Instagram 155.0.0.37.107'})
                                 # headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        for user in self.users:
            # if j_data.get('authenticated'):
            #     yield response.follow(
            #         f'/{self.user}',
            #         callback=self.user_parse,
            #         cb_kwargs={'username': self.user}
            #     )
            if j_data.get('authenticated'):
                yield response.follow(
                    f'/{user}',
                    callback=self.user_parse,
                    cb_kwargs={'username': user}
                )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12, 'search_surface': 'follow_list_page'}
        follower_page_link=f"{self.insta_followers_link}{user_id}/followers/?&{urlencode(variables)}"
        print()
        yield response.follow(follower_page_link,
                              callback=self.user_posts_parse,
                              cb_kwargs={
                                  'username': username,
                                  'user_id': user_id,
                                  'variables': deepcopy(variables)
                              }
                              )
        print()

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.insta_graf_ql_link}query_hash={self.posts_query_hash}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstaparserItem(
                user_id=user_id,
                username=username,
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                photo=post.get('node').get('display_url'),
                post_data=post.get('node')
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for login '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')