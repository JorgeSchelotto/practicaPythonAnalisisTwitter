from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class AzureAnalisis:
    # Para azure

    def __init__(self, key, endpoint):
        self.subscription_key = key
        self.endpoint = endpoint


    def authenticate_client(self):
        ta_credential = AzureKeyCredential(self.subscription_key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=self.endpoint, credential=ta_credential)
        return text_analytics_client

    
    def sentiment_analysis_example(self, client,text):

        documents = [text]
        response = client.analyze_sentiment(documents = documents)[0]
        
        return response




# subscription_key = "a1628afdd27b418d91dcfa4aab7b50f3"
# endpoint = "https://analisistwitter.cognitiveservices.azure.com/"

# analisis= AzureAnalisis(subscription_key, endpoint )

# client = analisis.authenticate_client()
# text = "zurdos de mierda"
# analisis.sentiment_analysis_example(client, text)