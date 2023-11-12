import os
import re
from dotenv import load_dotenv


from poTranslation.ms_t import translator as ms_t
from poTranslation.openai_t import translator as openai_t


class Translator:
    patterns = {
        'python': r'(%(?:\((?P<key>.*?)\))?[-#0 +]*?(?:\d+)?(?:\.\d+)?[hlL]?[diouxXeEfFgGcrs%])',
        # Add other language patterns here
    }
    
    def __init__(self, dest_language, source_language = 'en',lang='python', env_path=None):
        # region base init
        load_dotenv()
        
        if env_path is not None:
            os.environ['PATH'] += os.pathsep + env_path
        
        self.source_language = source_language
        self.dest_language = dest_language
        self.placeholder_pattern_string = self.patterns.get(lang)
        if self.placeholder_pattern_string is None:
            raise ValueError(f"Language {lang} is not supported.")
        self.placeholder_pattern  = re.compile(self.placeholder_pattern_string)
        self.service = os.environ.get('TRANSLATOR_SERVICE', 'MS').upper()
        # endregion

        # region service init
        if self.service == 'MS':
            self.api_key = os.environ.get('MS_API_KEY')
            self.api_region = os.environ.get('MS_API_REGION')
            
            if not self.api_region:
                raise ValueError("Error: MS_API_REGION is not set in environment variables.")
            if not self.api_key:
                raise ValueError("Error: MS_API_KEY is not set in environment variables.")
            
            self.service_t = ms_t(self.api_key, self.api_region, self.placeholder_pattern, self.source_language, self.dest_language)
            
        elif self.service == 'GOOGLE':
            raise ValueError("Google Translate is not supported yet.")
        elif self.service == 'OPENAI':
            
            self.api_key = os.environ.get('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("Error: OPENAI_API_KEY is not set in environment variables.")
            self.service_t = openai_t(self.api_key, self.source_language, self.dest_language, lang)
            
        else:
            raise ValueError("Error: TRANSLATOR_SERVICE is not valid.")
        # endregion

    def translate(self, text):
        preprocessed_text = self.service_t.preproc(text)
        
        translated_text, error = self.service_t.translate(preprocessed_text)
        if error:
            return "", error
        
        translated_text = self.service_t.postproc(translated_text)
        # return empty string if error

        return translated_text, error


