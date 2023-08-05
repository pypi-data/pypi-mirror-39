import pytest
import vcr

from fhrs.fhrs import Client


@pytest.fixture
def create_client():
    """Creates an initial client object"""
    return Client()


@vcr.use_cassette('vcr_casette/getregion.yml')
def test_getregions_size(create_client):
    _reg = create_client.getregions()
    assert len(_reg.index) == 12
    assert len(_reg.columns) == 5


@vcr.use_cassette('vcr_casette/getregion.yml')
def test_getregions_colnames(create_client):
    _reg = create_client.getregions()
    list_names = ["id", "name", "nameKey", "code", "links"]
    assert set(list_names).issubset(_reg.columns)


@vcr.use_cassette('vcr_casette/getregionbyid.yml')
def test_getregionbyid_idcheck(create_client):
    assert create_client.getregionbyid(3).loc[0, 'name'] == 'London'
    assert create_client.getregionbyid(5).loc[0, 'code'] == 'NW'


@vcr.use_cassette('vcr_casette/getregionbyid.yml')
def test_getregionbyid_collen(create_client):
    assert len(create_client.getregionbyid(3).columns) == 5


@vcr.use_cassette('vcr_casette/getregionsbasic.yml')
def test_getregionsbasic_size(create_client):
    _reg_basic = create_client.getregionsbasic()
    assert len(_reg_basic.index) == 12
    assert len(_reg_basic.columns) == 5


@vcr.use_cassette('vcr_casette/getregionsbasic.yml')
def test_getregionsbasic_(create_client):
    _reg_basic = create_client.getregionsbasic()
    list_names = ["id", "name", "nameKey", "code", "links"]
    assert set(list_names).issubset(_reg_basic.columns)


@vcr.use_cassette('vcr_casette/getauthorities.yml')
def test_getauthorities_size(create_client):
    _auth = create_client.getauthorities()
    assert len(_auth.columns) == 15
    assert len(_auth.index) == 392


@vcr.use_cassette('vcr_casette/getauthorities.yml')
def test_getauthorities_name(create_client):
    _auth = create_client.getauthorities()
    list_names = ["Adur", "Babergh", "Wealden", "West Devon", "Westminster", "Wyre", "York"]
    assert set(list_names).issubset(set(_auth['Name']))


@vcr.use_cassette('vcr_casette/getauthoritiesbasic.yml')
def test_getauthoritiesbasic_size(create_client):
    _auth = create_client.getauthoritiesbasic()
    assert len(_auth.columns) == 6
    assert len(_auth.index) == 392


@vcr.use_cassette('vcr_casette/getauthoritiesbasic.yml')
def test_getauthoritiesbasic_name(create_client):
    _auth = create_client.getauthoritiesbasic()
    list_names = ["Adur", "Babergh", "Wealden", "West Devon", "Westminster", "Wyre", "York"]
    assert set(list_names).issubset(set(_auth['Name']))


@vcr.use_cassette('vcr_casette/getauthoritybyid.yml')
def test_getauthoritybyid_name(create_client):
    _auth = create_client.getauthoritybyid(2)
    assert _auth.loc[0, 'Name'] == 'East Cambridgeshire'


@vcr.use_cassette('vcr_casette/getbusinesstypes.yml')
def test_getbusinesstypes_size(create_client):
    business = create_client.getbusinesstypes()
    assert len(business.columns) == 3
    assert len(business.index) == 15


@vcr.use_cassette('vcr_casette/getbusinesstypes.yml')
def test_getbusinesstypes_type(create_client):
    business = create_client.getbusinesstypes()
    list_names = ['Retailers - other', 'Takeaway/sandwich shop', 'School/college/university', 'Importers/Exporters',
                  'Farmers/growers']
    assert set(list_names).issubset(set(business['BusinessTypeName']))


@vcr.use_cassette('vcr_casette/getbusinesstypebasic.yml')
def test_getbusinesstypesbasic_size(create_client):
    business = create_client.getbusinesstypesbasic()
    assert len(business.columns) == 3
    assert len(business.index) == 15


@vcr.use_cassette('vcr_casette/getbusinesstypebasic.yml')
def test_getbusinesstypesbasic_id(create_client):
    _business = create_client.getbusinesstypesbasic()
    list_id = [7, 7838, 5, 1, 7842, 14, 7839, 7846, 7841, 7843, 4613, 7840, 7845, 7844]
    assert set(list_id).issubset(set(_business['BusinessTypeId']))


@vcr.use_cassette('vcr_casette/getbusinesstypebyid.yml')
def test_getbusinesstypebyid_name(create_client):
    _business = create_client.getbusinesstypebyid(7841)
    assert _business.loc[0, 'BusinessTypeName'] == 'Other catering premises'


@vcr.use_cassette('vcr_casette/getcountries.yml')
def test_getcountries_size(create_client):
    _countries = create_client.getcountries()
    assert len(_countries.columns) == 5
    assert len(_countries.index) == 4


@vcr.use_cassette('vcr_casette/getcountries.yml')
def test_getcountries_name(create_client):
    _countries = create_client.getcountries()
    names = ['England', 'Northern Ireland', 'Scotland', 'Wales']
    assert set(names).issubset(set(_countries['name']))


@vcr.use_cassette('vcr_casette/getcountrybyid.yml')
def test_getcountrybyid_name(create_client):
    _country = create_client.getcountrybyid(1)
    assert _country.loc[0, 'name'] == 'England'


@vcr.use_cassette('vcr_casette/getcountriesbasic.yml')
def test_getcountriesbasic_size(create_client):
    _countries = create_client.getcountriesbasic()
    assert len(_countries.columns) == 5
    assert len(_countries.index) == 4


@vcr.use_cassette('vcr_casette/getcountriesbasic.yml')
def test_getcountriesbasic_name(create_client):
    _countries = create_client.getcountriesbasic()
    names = ['England', 'Northern Ireland', 'Scotland', 'Wales']
    assert set(names).issubset(set(_countries['name']))


@vcr.use_cassette('vcr_casette/getestablishmentsbyid.yml')
def test_getestablishmentsbyid_name(create_client):
    _name = create_client.getestablishmentsbyid(996)
    assert _name['BusinessName'] == 'Howitt Primary Community School'


@vcr.use_cassette('vcr_casette/getschemetypes.yml')
def test_getschemetypes_size(create_client):
    _schemes = create_client.getschemetypes()
    assert len(_schemes.index) == 2
    assert len(_schemes.columns) == 4


@vcr.use_cassette('vcr_casette/getschemetypes.yml')
def test_getschemetypes_name(create_client):
    _schemes = create_client.getschemetypes()
    list_names = ['Food Hygiene Rating Scheme', 'Food Hygiene Information System']
    assert set(list_names).issubset(set(_schemes['schemeTypeName']))


@vcr.use_cassette('vcr_casette/getsortoptions.yml')
def test_getsortoptions_size(create_client):
    _options = create_client.getsortoptions()
    assert len(_options.index) == 6
    assert len(_options.columns) == 4


@vcr.use_cassette('vcr_casette/getsortoptions.yml')
def test_getsortoptions_name(create_client):
    _options = create_client.getsortoptions()
    name_options = ['Relevance', 'Rating (highest to lowest)', 'Rating (lowest to highest)', 'Name (A to Z)',
                    'Name (Z to A)', 'Distance']
    assert set(name_options).issubset(set(_options['sortOptionName']))


@vcr.use_cassette('vcr_casette/getscoredescriptorsbyid.yml')
def test_getscoredescriptorsbyid_size(create_client):
    _descript = create_client.getscoredescriptorbyid(996)
    assert len(_descript.index) == 3
    assert len(_descript.columns) == 5


@vcr.use_cassette('vcr_casette/getscoredescriptorsbyid.yml')
def test_getscoredescriptorsbyid_name(create_client):
    _descript = create_client.getscoredescriptorbyid(996)
    list_category = ['Confidence', 'Hygiene', 'Structural']
    assert set(list_category).issubset(set(_descript['ScoreCategory']))


@vcr.use_cassette('vcr_casette/getratings.yml')
def test_getratings_size(create_client):
    _rating = create_client.getratings()
    assert len(_rating.index) == 11
    assert len(_rating.columns) == 6


@vcr.use_cassette('vcr_casette/getratings.yml')
def test_getratings_name(create_client):
    _rating = create_client.getratings()
    list_name = ['4', '3', '2', '1', '0', 'Pass', 'Improvement Required', 'Awaiting Publication', 'Awaiting Inspection',
                 'Exempt']
    assert set(list_name).issubset(set(_rating['ratingName']))


@vcr.use_cassette('vcr_casette/getratingsoperators.yml')
def test_getratingsoperators_size(create_client):
    _operator = create_client.getratingsoperators()
    assert len(_operator.index) == 3
    assert len(_operator.columns) == 4


@vcr.use_cassette('vcr_casette/getratingsoperators.yml')
def test_getratingsoperators_name(create_client):
    _operator = create_client.getratingsoperators()
    list_name = [6, 8, 9]
    assert set(list_name).issubset(set(_operator['ratingOperatorId']))
