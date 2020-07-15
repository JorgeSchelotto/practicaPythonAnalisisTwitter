import sys
import tweepy
from textblob import TextBlob 
#Se importa sleep, datetime, TextBlob y matplotlib
import requests
# pprint is used to format the JSON response
from pprint import pprint
import os


# Para azure
subscription_key = "a1628afdd27b418d91dcfa4aab7b50f3"
endpoint = "https://analisistwitter.cognitiveservices.azure.com/"


class TweetsListener(tweepy.StreamListener):

    def on_connect(self):
        print("Estoy conectado!")

    def on_status(self, status):
        # Aca puedo analisar el texto, guardar los negativos y crear un grafico.

        # Obtengo nombre de usuario
        print('Nombre: ',status.user.screen_name)


        # Recupero cuerpo de tweet
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
                print(status.retweeted_status.extended_tweet["full_text"])
            except AttributeError:
                tweet = status.retweeted_status.text
                print(status.retweeted_status.text)
        else:
            try:
                tweet = status.extended_tweet["full_text"]
                print(status.extended_tweet["full_text"])
            except AttributeError:
                tweet = status.text
                print(status.text)

        # Analisis
        #
        analisis = TextBlob(tweet)
        analisis = analisis.sentiment
        print(analisis)


        # Obtengo el numero de retweets
        #
        print("Retweets: " + str(status.retweet_count) + " veces \n")

    def on_error(self, status_code):
        print("Error", status_code)



consumer_key = 'lWVV5n7BfUMRrJPFu7tEfQZCJ'
consumer_secret = '97rcjKLdoSuPC262O1A42BcLCVwyaZgOWJ45k8VVQVyw2nvRYM'
access_token = '190070697-dsoKMXZgdYUYkkDLjYKp7yDR5mJfrebEGI4FJzzL'
access_token_secret = '1Tc3xCYPj4LHpsMaWB7eAxlYfNJWl3jRxypvsiK8KlYsD'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


buscar = input('Ingrese palabra a buscar: ')


stream = TweetsListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)
streamingApi.filter(
    # follow=["151179935"],
    track=[buscar],
    # locations=[-99.36492421,19.04823668,-98.94030286,19.59275713], # Ciudad de Mexico
 is_async=True)