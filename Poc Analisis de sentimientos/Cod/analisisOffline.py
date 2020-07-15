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
api = tweepy.API(auth)


# Creo el libro excel y una hoja
outWorkbook = xlsxwriter.Workbook("filterTwits.xlsx")
outSheet = outWorkbook.add_worksheet()


# Escribo nombre de columnas en excel
outSheet.write("A1", "Nombre")
outSheet.write("B1", "Texto")
outSheet.write("C1", "Emocion")


#Se pregunta por la palabra a buscar
palabra = input("Buscar: ")


#Se define la cantida de tweets a capturar
numero_de_Tweets = int(input(u"Número de tweets a capturar: "))


 #Se define el idioma de los tweets a analizar
# lenguaje = input("Idioma [es/en]:")


def ObtenerTweets(palabra="OSDE",times=100):
    #Se define las listas que capturan la popularidad
    popularidad_list = []
    numeros_list = []
    numero = 1
    # Indice para escribir en  excel
    excelIndex = 2  
    for tweet in tweepy.Cursor(api.search, palabra, tweet_mode='extended').items(numero_de_Tweets):
        try:
            # Se toma el texto, se hace el analisis de sentimiento
            if 'retweeted_status' in tweet._json:
                text = "RT: " + tweet._json['retweeted_status']['full_text']
                print("RT: ", tweet._json['retweeted_status']['full_text'])
            else:
                text = "NO RT:" + tweet.full_text
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
                outSheet.write("C"+ str(excelIndex), analisis.sentiment_analysis_example(client, text).sentiment)
                excelIndex+=1
            print("*"*20)
            # analisis = TextBlob(tweet.text)
            # analisis = analisis.sentiment
            # popularidad = analisis.sentiment_analysis_example(client, tweet.text).confidence_scores
            # popularidad_list.append(popularidad)
            # numeros_list.append(numero)
            # numero = numero + 1
            # print(tweet.text)

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    # return (numeros_list,popularidad_list,numero)







# def GraficarDatos(numeros_list,popularidad_list,numero):
#     axes = plt.gca()
#     axes.set_ylim([-1, 2])
    
#     plt.scatter(numeros_list, popularidad_list)
#     popularidadPromedio = (sum(popularidad_list))/(len(popularidad_list))
#     popularidadPromedio = "{0:.0f}%".format(popularidadPromedio * 100)
#     time  = datetime.now().strftime("A : %H:%M\n El: %m-%d-%y")
#     plt.text(0, 1.25, 
#             "Sentimiento promedio:  " + str(popularidadPromedio) + "\n" + time, 
#             fontsize=12, 
#             bbox = dict(facecolor='none', 
#                         edgecolor='black', 
#                         boxstyle='square, pad = 1'))
    
#     plt.title("Sentimientos sobre " + palabra + " en twitter")
#     plt.xlabel("Numero de tweets")
#     plt.ylabel("Sentimiento")
#     plt.show()

if __name__ == "__main__":
    ObtenerTweets(palabra,numero_de_Tweets)

    # Cierro el excel para que se cree/guarde
    outWorkbook.close()