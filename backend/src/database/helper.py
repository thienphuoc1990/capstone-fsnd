from .models import Actor, Movie 
from .data import dummy_actor_data, dummy_movie_data
  
class DataHelper: 
    def add_dummy_actor_data(): 
        ''' 
        Function to add dummy actor data into Table 
        '''
        for data in dummy_actor_data: 
            actor = Actor(*data) 
            actor.insert() 
            print(f"Successfully Added Actor: {actor.name}")
  
    def add_dummy_movie_data(): 
        ''' 
        Function to add dummy movie data into Table 
        '''
        for data in dummy_movie_data: 
            movie = Movie(*data) 
            movie.insert() 
            print(f"Successfully Added Movie: {movie.title}")
  