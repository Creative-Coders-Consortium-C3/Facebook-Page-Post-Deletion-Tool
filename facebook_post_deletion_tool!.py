# -*- coding: utf-8 -*-
"""Facebook Post Deletion Tool!.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x7M-DZLPdpyKCHv_i620mBi_Jk18xJWO
"""

!pip install facebook-sdk python-dateutil pandas

"""Facebook Post Deletion Script"""

import requests
import datetime
from dateutil.parser import parse

class FacebookPostDeletionTool:
    def __init__(self):
        self.user_access_token = None
        self.user_id = None
        self.pages = []
        self.current_page = None
        self.posts = []
        self.log = []
        self.total_deleted_posts = 0
        self.session_deleted_posts = 0

    def authenticate(self, user_access_token):
        if self.user_access_token == user_access_token:
            return  # Already authenticated with this token

        self.user_access_token = user_access_token
        try:
            response = requests.get(f"https://graph.facebook.com/v20.0/me?access_token={self.user_access_token}")
            response.raise_for_status()
            self.user_id = response.json()['id']
            self.log.append(f"Authentication successful. User ID: {self.user_id}")

            response = requests.get(f"https://graph.facebook.com/v20.0/{self.user_id}/accounts?access_token={self.user_access_token}")
            response.raise_for_status()
            self.pages = response.json()['data']
            self.log.append(f"Retrieved {len(self.pages)} pages")
        except requests.RequestException as e:
            self.log.append(f"Authentication failed: {str(e)}")
            raise

    def load_pages(self):
        return [{'name': page['name'], 'id': page['id']} for page in self.pages]

    def select_page(self, page_id):
        self.current_page = next((page for page in self.pages if page['id'] == page_id), None)
        if self.current_page:
            self.log.append(f"Selected page: {self.current_page['name']}")
        else:
            raise ValueError("Invalid page ID")

    def load_posts(self, limit=None):
        if not self.current_page:
            raise ValueError("No page selected")

        try:
            posts = []
            url = f"https://graph.facebook.com/v20.0/{self.current_page['id']}/feed"
            params = {
                'access_token': self.current_page['access_token'],
                'fields': 'id,message,full_picture,attachments{media_type,type},admin_creator,from{id,name,picture},created_time,reactions.limit(0).summary(total_count),comments.limit(0).summary(true),insights.metric(post_impressions_unique)',
                'limit': 100
            }

            while url:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                posts.extend(data['data'])
                if 'next' in data.get('paging', {}):
                    url = data['paging']['next']
                else:
                    break
                if limit and len(posts) >= limit:
                    break

            self.posts = posts[:limit] if limit else posts
            self.log.append(f"Loaded {len(self.posts)} posts")
            return self.posts
        except requests.RequestException as e:
            self.log.append(f"Error loading posts: {str(e)}")
            raise

    def delete_posts(self, filters):
        deleted_count = 0
        for post in self.posts:
            if self._apply_filters(post, filters):
                try:
                    attachment_type = self._get_attachment_type(post)
                    if attachment_type != 'profile_picture':  # Exclude profile picture updates
                        url = f"https://graph.facebook.com/v20.0/{post['id']}"
                        response = requests.delete(url, params={'access_token': self.current_page['access_token']})
                        response.raise_for_status()
                        deleted_count += 1
                        self.total_deleted_posts += 1
                        self.session_deleted_posts += 1
                        self.log.append(f"Deleted post: {post['id']}")
                except requests.RequestException as e:
                    self.log.append(f"Error deleting post {post['id']}: {str(e)}")

        self.log.append(f"Total posts deleted in this run: {deleted_count}")
        return deleted_count

    def _apply_filters(self, post, filters):
        if 'start_date' in filters and 'end_date' in filters:
            post_date = parse(post['created_time'])
            if not (filters['start_date'] <= post_date <= filters['end_date']):
                return False

        if 'post_type' in filters:
            attachment_type = self._get_attachment_type(post)
            if filters['post_type'] != 'all' and filters['post_type'] != attachment_type:
                return False

        if 'reaction_threshold' in filters:
            reaction_count = post.get('reactions', {}).get('summary', {}).get('total_count', 0)
            if reaction_count < filters['reaction_threshold']:
                return False

        return True

    def _get_attachment_type(self, post):
        if 'attachments' in post and 'data' in post['attachments']:
            attachment = post['attachments']['data'][0]
            if attachment.get('type') == 'profile_media':
                return 'profile_picture'
            elif attachment.get('type') == 'video_inline':
                return 'video'  # Treating reel and video as the same
            elif attachment.get('type') == 'photo':
                return 'photo'
            elif attachment.get('type') == 'share':
                return 'link'
        return 'status'

    def get_log(self):
        return self.log

    def get_stats(self):
        return {
            'total_deleted_posts': self.total_deleted_posts,
            'session_deleted_posts': self.session_deleted_posts
        }

def main():
    tool = FacebookPostDeletionTool()
    user_access_token = None

    while True:
        if not user_access_token:
            user_access_token = input("Enter your Facebook user access token (or 'q' to quit): ")
            if user_access_token.lower() == 'q':
                break
            try:
                tool.authenticate(user_access_token)
            except Exception as e:
                print(f"Authentication failed: {str(e)}")
                print("Please check your access token and try again.")
                user_access_token = None
                continue

        try:
            pages = tool.load_pages()
            print("\nAvailable Pages:")
            for i, page in enumerate(pages):
                print(f"{i+1}. {page['name']}")

            page_index = int(input("Select a page (enter number): ")) - 1
            if 0 <= page_index < len(pages):
                tool.select_page(pages[page_index]['id'])
            else:
                print("Invalid page selection.")
                continue

            load_all = input("Load all posts? (y/n): ").lower() == 'y'
            if load_all:
                posts = tool.load_posts()
            else:
                limit = int(input("Enter number of posts to load: "))
                posts = tool.load_posts(limit)

            print(f"Loaded {len(posts)} posts")

            filters = {}
            if input("Apply date filter? (y/n): ").lower() == 'y':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                filters['start_date'] = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                filters['end_date'] = datetime.datetime.strptime(end_date, '%Y-%m-%d')

            post_type = input("Filter by post type? (photo/video/status/link/all): ")
            filters['post_type'] = post_type

            if input("Apply reaction threshold filter? (y/n): ").lower() == 'y':
                filters['reaction_threshold'] = int(input("Enter minimum number of reactions: "))

            deleted_count = tool.delete_posts(filters)
            print(f"Deleted {deleted_count} posts in this run")

            stats = tool.get_stats()
            print(f"\nTotal posts deleted: {stats['total_deleted_posts']}")
            print(f"Posts deleted in this session: {stats['session_deleted_posts']}")

            print("\nOperation Log:")
            for log_entry in tool.get_log():
                print(log_entry)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        if input("\nProcess another page? (y/n): ").lower() != 'y':
            break

    print("Thank you for using the Facebook Post Deletion Tool!")

if __name__ == "__main__":
    main()