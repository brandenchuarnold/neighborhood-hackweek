from collections import namedtuple
from flask import jsonify
from logging import getLogger
from zillowdb.session.manager import DBTransaction

LOG = getLogger(__name__)


class PropertyRegion(namedtuple('PropertyRegion',
                                ['property_id',
                                 'region_id_neighborhood',
                                 'selling_price_dollar_cnt',
                                 'zestimate_dollar_cnt',
                                 'tax_paid_amt',
                                 'bedrooms',
                                 'bathrooms',
                                 'latitude',
                                 'longitude'])):

    __slots__ = ()

    def new(cls,
            property_id,
            region_id_neighborhood,
            selling_price_dollar_cnt,
            zestimate_dollar_cnt,
            tax_paid_amt,
            bedrooms,
            bathrooms,
            latitude,
            longitude):
        return super(PropertyRegion, cls).__new__(cls,
                                                  property_id,
                                                  region_id_neighborhood,
                                                  selling_price_dollar_cnt,
                                                  zestimate_dollar_cnt,
                                                  tax_paid_amt,
                                                  bedrooms,
                                                  bathrooms,
                                                  latitude,
                                                  longitude)

def _create_property_region_from_sql(property_region):
    return PropertyRegion(
        property_id=int(property_region['PropertyID']) if property_region['PropertyID'] else None,
        region_id_neighborhood=int(property_region['RegionIDNeighborhood']) if property_region['RegionIDNeighborhood'] else None,
        selling_price_dollar_cnt=int(property_region['SellingPriceDollarCnt']) if property_region['SellingPriceDollarCnt'] else None,
        zestimate_dollar_cnt=int(property_region['ZestimateDollarCnt']) if property_region['ZestimateDollarCnt'] else None,
        tax_paid_amt=float(property_region['TaxPaidAmt']) if property_region['TaxPaidAmt'] else None,
        bedrooms=int(property_region['Bedrooms']) if property_region['Bedrooms'] else None,
        bathrooms=int(property_region['Bathrooms']) if property_region['Bathrooms'] else None,
        latitude=int(property_region['Latitude']) if property_region['Latitude'] else None,
        longitude=int(property_region['Longitude']) if property_region['Longitude'] else None
    )


@DBTransaction('property_db')
def get_property_regions_by_region_id_neighborhood(region_id_neighborhood,
                                                   session=None):
    """Get all zpids in a neighborhood"""
    query = ('exec dbo.PropertyRegionGetByRegionIDNeighborhood'
             ' :region_id_neighborhood')
    params = dict(region_id_neighborhood=region_id_neighborhood)
    results = session.execute(query, params)
    return [property_region._asdict() for property_region in map(_create_property_region_from_sql, results)] if results else []
