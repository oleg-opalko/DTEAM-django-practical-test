from openai import OpenAI
from django.conf import settings
import json


LANGUAGE_CODES = {
    'Cornish': 'kw',
    'Manx': 'gv',
    'Breton': 'br',
    'Inuktitut': 'iu',
    'Kalaallisut': 'kl',
    'Romani': 'rom',
    'Occitan': 'oc',
    'Ladino': 'lad',
    'Northern Sami': 'se',
    'Upper Sorbian': 'hsb',
    'Kashubian': 'csb',
    'Zazaki': 'zza',
    'Chuvash': 'cv',
    'Livonian': 'liv',
    'Tsakonian': 'tsd',
    'Saramaccan': 'srm',
    'Bislama': 'bi'
}

def translate_text(text, target_language):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text to {target_language}. Maintain the original formatting and structure."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        if "insufficient_quota" in error_message:
            raise Exception("Translation service is currently unavailable due to API quota limits. Please try again later.")
        elif "invalid_api_key" in error_message:
            raise Exception("Translation service is not properly configured. Please contact the administrator.")
        else:
            raise Exception(f"Translation failed: {error_message}")

def translate_cv(cv, target_language):
    try:
        cv_content = {
            'first_name': cv.first_name,
            'last_name': cv.last_name,
            'skills': cv.skills,
            'projects': cv.projects,
            'bio': cv.bio,
            'contacts': cv.contacts,
        }
        
        cv_json = json.dumps(cv_content, ensure_ascii=False)
        
        translated_json = translate_text(cv_json, target_language)
        
        if translated_json:
            try:
                return json.loads(translated_json)
            except json.JSONDecodeError:
                raise Exception("Failed to process translated content. Please try again.")
        
        return None
    except Exception as e:
        raise Exception(str(e)) 