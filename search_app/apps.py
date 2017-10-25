from django.apps import AppConfig
from watson import search as watson



class SearchConfig(AppConfig):
    name = 'search_app'
    
    def ready(self):
        YourModel = self.get_model("hobbytag")
        watson.register(YourModel)
        YourModel2 = self.get_model("features")
        watson.register(YourModel2)
        YourModel3 = self.get_model("extra_tag")
        watson.register(YourModel3)
        YourModel4 = self.get_model("states")
        watson.register(YourModel4)

