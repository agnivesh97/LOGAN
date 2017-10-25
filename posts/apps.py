from django.apps import AppConfig
from watson import search as watson


class PostsConfig(AppConfig):
    name = 'posts'
    def ready(self):
        YourModel = self.get_model("Place")
        watson.register(YourModel)
        YourModel2 = self.get_model("People")
        watson.register(YourModel2)
        
