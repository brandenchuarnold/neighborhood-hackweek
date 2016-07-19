from collections import namedtuple
from logging import getLogger
from zillowdb.session.manager import DBTransaction

LOG = getLogger(__name__)


class PropertyRegion(namedtuple('PropertyRegion',
                                ['PropertyID',
                                 'DataSourceTypeID',
                                 'BestRecordFlag',
                                 'RegionIDState',
                                 'RegionIDCounty',
                                 'RegionIDCity',
                                 'RegionIDNeighborhood',
                                 'RegionIDZip',
                                 'StreetID',
                                 'RegionIDSchoolFragment',
                                 'RegionIDSubdivision',
                                 'RegionIDMasterCommmunity',
                                 'UpdateDate',
                                 'LastUpdateBy',
                                 'LastUpdateAccountID'])):

    __slots__ = ()

    def new(cls,
            property_id,
            data_source_id,
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
                                                  data_source_id,
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
            property_id=int(property_region['PropertyID']),
            data_source_id=int(property_region['DataSourceID']),
            best_record_flag=bool(property_region['BestRecordFlag']),
            region_id_state=int(property_region['RegionIDState']),
            region_id_county=int(property_region['RegionIDCounty']),
            region_id_city=int(property_region['RegionIDCity']),
            region_id_neighborhood=int(property_region['RegionIDNeighborhood']),
            region_id_zip=int(property_region['RegionIDZip']),
            street_id=int(property_region['StreetID']),
            region_id_school_fragment=int(property_region['RegionIDSchoolFragment']),
            region_id_subdivision=int(property_region['RegionIDSubdivision']),
            region_id_master_community=int(property_region['RegionIDMasterCommunity']),
            update_date=property_region['UpdateDate'],
            last_update_by=property_region['LastUpdateBy'],
            last_update_account_id=int(property_region['LastUpdateAccountID']))


@DBTransaction('property_db')
def get_property_regions_by_region_id_neighborhood(region_id_neighborhood,
                                                   session=None):
    """Get all zpids in a neighborhood"""
    query = ('exec dbo.PropertyRegionGetByRegionIDNeighborhood'
             ' :region_id_neighborhood')
    params = dict(region_id_neighborhood=region_id_neighborhood)
    results = session.execute(query, params)
    return map(_create_property_region_from_sql, results) if results else []
