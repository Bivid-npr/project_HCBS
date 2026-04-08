class Film:
    def __init__(self, film_id, title, description, genre, age_rating, imdb_rating, duration, cast_members, release_year):
        self.film_id= film_id
        self.title= title
        self.description= description
        self.genre = genre
        self.age_rating = age_rating
        self.imdb_rating= imdb_rating
        self.duration =duration
        self.cast_members= cast_members
        self.release_year =release_year
        
        
    def get_film_id(self) -> int:
        return self.film_id
    
    def get_title(self) -> str:
        return self.title
    
    def __str__(self) -> str:
        return(f"{self.title} ({self.release_year}) | {self.genre} |"
               f" Rated: {self.age_rating} |IMDb : {self.imdb_rating} |"
               f"{self.duration} mins")
        