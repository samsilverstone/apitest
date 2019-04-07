from api import app

def create_app(config_object=None):

    final_app = app 
    if config_object != None:
        final_app.config.from_object(config_object)
        
    return final_app
