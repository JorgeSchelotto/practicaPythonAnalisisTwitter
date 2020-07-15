#Se importa la librería tweepy
#
import tweepy
#Se importa sleep, datetime, TextBlob y matplotlib
#
from time import sleep
from datetime import datetime
from textblob import TextBlob 
import matplotlib.pyplot as plt 
from azureTextAnalitic import AzureAnalisis
import xlsxwriter
import numpy as np
from datetime import date
from datetime import datetime

# Día actual
today = date.today()

# Azure keys
subscription_key = "a1628afdd27b418d91dcfa4aab7b50f3"
endpoint = "https://analisistwitter.cognitiveservices.azure.com/"

# Twitter API keys
consumer_key = 'lWVV5n7BfUMRrJPFu7tEfQZCJ'
consumer_secret = '97rcjKLdoSuPC262O1A42BcLCVwyaZgOWJ45k8VVQVyw2nvRYM'
access_token = '190070697-dsoKMXZgdYUYkkDLjYKp7yDR5mJfrebEGI4FJzzL'
access_token_secret = '1Tc3xCYPj4LHpsMaWB7eAxlYfNJWl3jRxypvsiK8KlYsD'


# instancio azure analitics
analisis = AzureAnalisis(subscription_key,endpoint)
client = analisis.authenticate_client()


# Se autentica en twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


# Creo el libro excel y una hoja
outWorkbook = xlsxwriter.Workbook("filterTwits.xlsx")
outSheet = outWorkbook.add_worksheet()


# Escribo nombre de columnas en excel
outSheet.write("A1", "Nombre")
outSheet.write("B1", "Texto")
outSheet.write("C1", "Emocion")
outSheet.write("D1", "Score Positivo")
outSheet.write("E1", "Score Neutral")
outSheet.write("F1", "Score Negativo")


#Se pregunta por la palabra a buscar
palabra = input("Buscar: ")


#Se define la cantida de tweets a capturar
numero_de_Tweets = int(input(u"Número de tweets a capturar: "))


 #Se define el idioma de los tweets a analizar
# lenguaje = input("Idioma [es/en]:")


def ObtenerTweets(palabra="OSDE",times=100):
    #Se define las listas que capturan la popularidad
    positivos_list = []
    neutros_list = []
    negativos_list = []
    total = 0
    # Indice para escribir en  excel
    excelIndex = 2  
    for tweet in tweepy.Cursor(api.search, palabra, tweet_mode='extended').items(numero_de_Tweets):
        try:
            # Se toma el texto, se hace el analisis de sentimiento
            if 'retweeted_status' in tweet._json:
                text = "RT: " + tweet._json['retweeted_status']['full_text']
                print("RT: ", tweet._json['retweeted_status']['full_text'])
            else:
                text = "NO RT: " + tweet.full_text
                print("NO RT: " + tweet.full_text)
            # print(tweet.full_text)
            
            print(tweet.user.screen_name, analisis.sentiment_analysis_example(client, text).sentiment)

            if ((analisis.sentiment_analysis_example(client, text).sentiment == "negative") 
            or (analisis.sentiment_analysis_example(client, text).sentiment == "mixed") 
            or (analisis.sentiment_analysis_example(client, text).sentiment == "neutral")):
                # Escribo excel segun se necesite
                # Nombre
                outSheet.write("A"+ str(excelIndex), tweet.user.screen_name)
                # Texto
                outSheet.write("B"+ str(excelIndex), text)
                # Emocion
                # print(analisis.sentiment_analysis_example(client, text))
                outSheet.write("C"+ str(excelIndex), analisis.sentiment_analysis_example(client, text).sentiment)

                # Positivos
                #
                scoresPositive = analisis.sentiment_analysis_example(client, text).confidence_scores.positive
            
                # Neutral
                #
                scoresNeutral = analisis.sentiment_analysis_example(client, text).confidence_scores.neutral

                # Negativos
                #
                scoresNegative = analisis.sentiment_analysis_example(client, text).confidence_scores.negative


                outSheet.write("D"+ str(excelIndex), scoresPositive)
                outSheet.write("E"+ str(excelIndex), scoresNeutral)
                outSheet.write("F"+ str(excelIndex), scoresNegative)
                # keyPhrases = analisis.sentiment_analysis_example(client, text).key_phrases[0]
                # outSheet.write("F"+ str(excelIndex), keyPhrases) 
                excelIndex+=1
            print("*"*20)

            
            # Score Positive
            positivos_list.append(analisis.sentiment_analysis_example(client, text).confidence_scores.positive)
            # Score Neutral
            neutros_list.append(analisis.sentiment_analysis_example(client, text).confidence_scores.neutral)
            # Score negative
            negativos_list.append(analisis.sentiment_analysis_example(client, text).confidence_scores.negative)
            # Sumo total de procesados
            total+=1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    return (positivos_list, neutros_list, negativos_list, total)







def GraficarDatos(positivos_list,neutros_list,negativos_list,total):

    # Saco totales
    #
    totalPositivos = sum(positivos_list)
    totalNeutros = sum(neutros_list)
    totalNegativos = sum(negativos_list)

    # Saco promedios
    #
    promPositivos= (totalPositivos/total)*100
    promNeutros= (totalNeutros/total)*100
    promNegativos= (totalNegativos/total)*100


    # Grafico
    #
    fig = plt.figure("Analisis Twitter")
    grupo1 = fig.add_subplot(111)
    plt.title("Analisis de sensaciones Twitter")


    sensaciones = ["Positivos", "Neutrales", "Negativos"]
    calif1 = np.array([promPositivos, promNeutros, promNegativos])


    grupo1.bar(sensaciones, calif1, align="center", color=['green','orange','red'])
    grupo1.set_xticks(sensaciones)
    grupo1.set_xticklabels(sensaciones)
    grupo1.set_ylabel("SCORE PROMEDIADO")

    plt.savefig("Analisis_Twitter_"+str(today)+".jpg")
    plt.show()
    
    return promNegativos








if __name__ == "__main__":
    positivos, neutros, negativos, total = ObtenerTweets(palabra,numero_de_Tweets)
    print(positivos, neutros, negativos, total)
    negativos = GraficarDatos(positivos, neutros, negativos, total)

    print("negativos : " + str(round(negativos)))
    # Cierro el excel para que se cree/guarde
    outWorkbook.close()