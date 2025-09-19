import os
class TemplateParser:
    def __init__(self , lang : str =  None , def_lang:str ='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.defulat_lang = def_lang
        self.lang = None

        self.set_lang(lang)

    def set_lang(self,lang : str) : 
        if not lang :
            self.lang= self.defulat_lang
        
        language_path = os.path.join(self.current_path,'locales' , lang)
        if lang and os.path.exists(language_path) :
            self.lang = lang
        else : 
            self.lang= self.defulat_lang



    def get(self, group :str , key :str , vars :dict = {}) : 
        if not group or not key :
            return None
        
        group_path = os.path.join(self.current_path ,'locales', self.lang , f"{group}.py")
        targeted_language = self.lang

        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py" )
            targeted_language = self.default_language


        if not os.path.exists(group_path):
            return None
        
        module = __import__(f"stores.llm.TemplateParser.locales.{targeted_language}.{group}",
                             fromlist=[group])
        
        if not module:
            return None
        
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars)
        



