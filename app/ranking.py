import configparser
import time
from datetime import datetime, timezone

import tweepy
import coc

from utils import *

class Ranking:
	#seconds to wait from tweet to tweet
	wait_time = 1

	def __init__(self, config_file, texts_file):
		#read from config
		config = configparser.ConfigParser()
		config.read(config_file, encoding='utf-8')

		texts = configparser.ConfigParser()
		texts.read(texts_file, encoding='utf-8')

		self.consumer_key = config['twitter']['consumer_key']
		self.consumer_secret = config['twitter']['consumer_secret']
		self.bearer_token = config['twitter']['bearer_token']
		self.access_token = config['twitter']['access_token']
		self.access_token_secret = config['twitter']['access_token_secret']

		self.email = config['coc']['email']
		self.password = config['coc']['password']

		self.header_title = texts['texts']['header_title'].replace('\\n', '\n')
		self.header_time = texts['texts']['header_time'].replace('\\n', '\n')
		self.ranking_line = texts['texts']['ranking_line'].replace('\\n', '\n')
		self.footer = texts['texts']['footer'].replace('\\n', '\n')

		#login
		self.twitter_client = tweepy.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, access_token=self.access_token, access_token_secret=self.access_token_secret)
		self.coc_client = coc.login(self.email, self.password)

	async def post_global_player(self):
		players = await self.coc_client.get_location_players(limit=5)

		text = self.get_header("player")
		list_names = [x.name for x in players]
		list_trophies = [x.trophies for x in players]
		text += self.get_ranking(list_names, list_trophies)
		text += self.get_footer()

		self.publish_text(text)

	async def post_global_player_versus(self):
		players = await self.coc_client.get_location_players_versus(limit=5)

		text = self.get_header("player versus")
		list_names = [x.name for x in players]
		list_trophies = [x.versus_trophies for x in players]
		text += self.get_ranking(list_names, list_trophies)
		text += self.get_footer()

		self.publish_text(text)

	async def post_global_clan(self):
		clans = await self.coc_client.get_location_clans(limit=5)

		text = self.get_header("clan")
		list_names = [x.name for x in clans]
		list_trophies = [x.points for x in clans]
		text += self.get_ranking(list_names, list_trophies)
		text += self.get_footer()

		self.publish_text(text)

	async def post_global_clan_versus(self):
		clans = await self.coc_client.get_location_clans_versus(limit=5)

		text = self.get_header("clan versus")
		list_names = [x.name for x in clans]
		list_trophies = [x.versus_points for x in clans]
		text += self.get_ranking(list_names, list_trophies)
		text += self.get_footer()

		self.publish_text(text)

	def post(self, func, wait=True):
		self.coc_client.loop.run_until_complete(func)
		if(wait):
			time.sleep(wait_time)


	def start(self):
		self.post(self.post_global_clan_versus())
		self.post(self.post_global_player_versus())
		self.post(self.post_global_clan())
		self.post(self.post_global_player(), False)


	def get_header(self, type):
		now_utc = datetime.now(timezone.utc)

		text = self.header_title.format(type)
		text += now_utc.strftime(self.header_time)

		return text

	def get_ranking(self, list_names, list_trophies):
		text = ""

		for i, name, trophies in zip(range(len(list_names)), list_names, list_trophies):
			text += self.ranking_line.format(fullwidth(i+1), name, trophies)

		return text

	def get_footer(self):
		return self.footer

	def publish_text(self, text):
		print(text)
		#self.twitter_client.create_tweet(text=text)
