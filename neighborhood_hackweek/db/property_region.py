from collections import namedtuple
from logging import getLogger
from zillowdb.session.manager import DBTransaction

LOG = getLogger(__name__)


class PropertyRegion(namedtuple('PropertyRegion',
                                ['property_id',
                                 'data_source_type_id',
                                 'best_record_flag',
                                 'region_id_state',
                                 'region_id_county',
                                 'region_id_city',
                                 'region_id_neighborhood',
                                 'region_id_zip',
                                 'street_id',
                                 'region_id_school_fragment',
                                 'region_id_subdivision',
                                 'region_id_master_community',
                                 'update_date',
                                 'last_update_by',
                                 'last_update_account_id'])):

    __slots__ = ()

    def new(cls,
            property_id,
            data_source_type_id,
            best_record_flag,
            region_id_state,
            region_id_county,
            region_id_city,
            region_id_neighborhood,
            region_id_zip,
            street_id,
            region_id_school_fragment,
            region_id_subdivision,
            region_id_master_community,
            update_date,
            last_update_by,
            last_update_account_id):
        return super(PropertyRegion, cls).__new__(cls,
                                                  property_id,
                                                  data_source_type_id,
                                                  best_record_flag,
                                                  region_id_state,
                                                  region_id_county,
                                                  region_id_city,
                                                  region_id_neighborhood,
                                                  region_id_zip,
                                                  street_id,
                                                  region_id_school_fragment,
                                                  region_id_subdivision,
                                                  region_id_master_community,
                                                  update_date,
                                                  last_update_by,
                                                  last_update_account_id)

def _create_property_region_from_sql(property_region):
    return PropertyRegion(
        property_id=int(property_region['PropertyID']) if property_region['PropertyID'] else None,
        data_source_type_id=int(property_region['DataSourceTypeID']) if property_region['DataSourceTypeID'] else None,
        best_record_flag=bool(property_region['BestRecordFlag']),
        region_id_state=int(property_region['RegionIDState']) if property_region['RegionIDState'] else None,
        region_id_county=int(property_region['RegionIDCounty']) if property_region['RegionIDCounty'] else None,
        region_id_city=int(property_region['RegionIDCity']) if property_region['RegionIDCity'] else None,
        region_id_neighborhood=int(property_region['RegionIDNeighborhood']) if property_region['RegionIDNeighborhood'] else None,
        region_id_zip=int(property_region['RegionIDZip']) if property_region['RegionIDZip'] else None,
        street_id=int(property_region['StreetID']) if property_region['StreetID'] else None,
        region_id_school_fragment=int(property_region['RegionIDSchoolFragment']) if property_region['RegionIDSchoolFragment'] else None,
        region_id_subdivision=int(property_region['RegionIDSubdivision']) if property_region['RegionIDSubdivision'] else None,
        region_id_master_community=int(property_region['RegionIDMasterCommunity']) if property_region['RegionIDMasterCommunity'] else None,
        update_date=property_region['UpdateDate'],
        last_update_by=property_region['LastUpdateBy'],
        last_update_account_id=int(property_region['LastUpdateAccountID']) if property_region['LastUpdateAccountID'] else None)


@DBTransaction('property_db')
def get_property_regions_by_region_id_neighborhood(region_id_neighborhood,
                                                   session=None):
    """Get all zpids in a neighborhood"""
    query = ('exec dbo.PropertyRegionGetByRegionIDNeighborhood'
             ' :region_id_neighborhood')
    params = dict(region_id_neighborhood=region_id_neighborhood)
    results = session.execute(query, params)
    return [property_region._asdict() for property_region in map(_create_property_region_from_sql, results)] if results else []
