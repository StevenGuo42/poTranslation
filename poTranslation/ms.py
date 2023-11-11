import json
import requests

class translator:
    def __init__(self, api_key, api_region, placeholder_pattern, source_language, dest_language):
        self.api_key = api_key
        self.api_region = api_region
        self.placeholder_pattern = placeholder_pattern
        self.source_language = source_language
        self.dest_language = dest_language
        
    
    def translate(self, text):
        if not self.api_key:
            return None, "API_KEY is not set in environment variables."

        auth = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.api_region
        }

        try:
            r = requests.post(
                f'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={self.source_language}&to={self.dest_language}',
                headers=auth,
                json=[{'Text': text}]
            )
            if r.status_code != 200:
                return None, 'Error: the translation service failed.'
            translated_text = r.json()[0]['translations'][0]['text']
            return translated_text, None
        except Exception as e:
            return None, str(e)


    def preproc(self, text):
        # Replace placeholders with <mstrans:dictionary> tags
        return self.placeholder_pattern.sub(
            r'<mstrans:dictionary translation="\1">\1</mstrans:dictionary>', text)
        
    def postproc(self, text):
        return text