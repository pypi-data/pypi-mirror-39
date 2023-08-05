import pandas as pd
import requests


class Client(object):
    def __init__(self):
        self.session = requests.Session()
        self.url_base = 'http://api.ratings.food.gov.uk/'
        self.headers = {'x-api-version': '2', 'accept': 'application/json'}

    def getregions(self):
        region = self.session.get(self.url_base + 'Regions/', headers=self.headers)
        region = pd.DataFrame.from_dict(region.json()['regions'])
        return region

    def getregionbyid(self, _id):
        region = self.session.get(self.url_base + 'Regions/' + str(_id), headers=self.headers)
        region = pd.DataFrame.from_dict(region.json())
        return region

    def getregionsbasic(self):
        region = self.session.get(self.url_base + 'Regions/basic', headers=self.headers)
        region = pd.DataFrame.from_dict(region.json()['regions'])
        return region

    def getauthorities(self):
        auth = self.session.get(self.url_base + 'Authorities/', headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json()['authorities'])
        return auth

    def getauthoritiesbasic(self):
        auth = self.session.get(self.url_base + 'Authorities/basic', headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json()['authorities'])
        return auth

    def getauthoritybyid(self, _id):
        auth = self.session.get(self.url_base + 'Authorities/' + str(_id), headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json())
        return auth

    def getbusinesstypes(self):
        business = self.session.get(self.url_base + 'BusinessTypes', headers=self.headers)
        business = pd.DataFrame.from_dict(business.json()['businessTypes'])
        return business

    def getbusinesstypesbasic(self):
        business = self.session.get(self.url_base + 'BusinessTypes/basic', headers=self.headers)
        business = pd.DataFrame.from_dict(business.json()['businessTypes'])
        return business

    def getbusinesstypebyid(self, _id):
        business = self.session.get(self.url_base + 'BusinessTypes/' + str(_id), headers=self.headers)
        business = pd.DataFrame.from_dict(business.json())
        return business

    def getcountries(self):
        countries = self.session.get(self.url_base + 'Countries', headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json()['countries'])
        return countries

    def getcountrybyid(self, _id):
        countries = self.session.get(self.url_base + 'Countries/' + str(_id), headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json())
        return countries

    def getcountriesbasic(self):
        countries = self.session.get(self.url_base + 'Countries/basic', headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json()['countries'])
        return countries

    def getestablishmentsbyid(self, _id):
        establishment = self.session.get(self.url_base + 'Establishments/' + str(_id), headers=self.headers)
        return establishment.json()

    def getschemetypes(self):
        schemetypes = self.session.get(self.url_base + 'SchemeTypes', headers=self.headers)
        schemetypes = pd.DataFrame.from_dict(schemetypes.json()['schemeTypes'])
        return schemetypes

    def getsortoptions(self):
        options = self.session.get(self.url_base + 'SortOptions', headers=self.headers)
        options = pd.DataFrame.from_dict(options.json()['sortOptions'])
        return options

    def getscoredescriptorbyid(self, _id):
        scoredescriptor = self.session.get(self.url_base + 'ScoreDescriptors?establishmentId=' + str(_id),
                                           headers=self.headers)
        scoredescriptor = pd.DataFrame.from_dict(scoredescriptor.json()['scoreDescriptors'])
        return scoredescriptor

    def getratings(self):
        ratings = self.session.get(self.url_base + 'Ratings', headers=self.headers)
        ratings = pd.DataFrame.from_dict(ratings.json()['ratings'])
        return ratings

    def getratingsoperators(self):
        ratingoperator = self.session.get(self.url_base + 'RatingOperators', headers=self.headers)
        ratingoperator = pd.DataFrame.from_dict(ratingoperator.json()['ratingOperator'])
        return ratingoperator
