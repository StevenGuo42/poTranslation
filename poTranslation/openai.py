from openai import OpenAI
from json import loads as json_loads


class translator:
    def __init__(self, api_key, source_language, dest_language, lang='python'):
        self.client = OpenAI(api_key=api_key)
        self.sys_prompt = f'''You are a professional translator. You are tasked with translating text from `{source_language}` to `{dest_language}` for program localization. The following is a {lang} string. If there are any string formatting placeholders, please keep them as is. Now translate the string in the triple backticks below:'''

    
    def translate(self, text):
        try:
            response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": f"""```{text}```"""},
                {"role": "system", "content": "You would return a JSON file with only one object `text` for translated string."}
            ],
            )
            return json_loads(response.choices[0].message.content)['text'], None
        except Exception as e:
            return None, str(e)
        

    def preproc(self, text):
        return text
        
    def postproc(self, text):
        return text
