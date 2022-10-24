class MovieClass:

    def __init__(self, sub_name, sub_lang,sub_creator,times_dl,created_at,download_link):
        self.sub_name = sub_name
        self.sub_lang = sub_lang
        self.sub_creator = sub_creator
        self.times_dl = times_dl
        self.created_at = created_at
        self.download_link = download_link

    def setRating(self, rating):
        self.rating = rating

    def setReviews(self, no_reviews):
        self.no_reviews = no_reviews

    def setGenre(self, genre):
        self.genre = genre