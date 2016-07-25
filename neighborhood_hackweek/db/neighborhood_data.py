from collections import namedtuple
from flask import jsonify
from logging import getLogger
from zillowdb.session.manager import DBTransaction

LOG = getLogger(__name__)


class NeighborhoodData(namedtuple('NeighborhoodData',
                                  ['region_id',
                                   'median_monthly_income',
                                   'mean_house_hold_size',
                                   'mean_min_bed',
                                   'mean_max_bed',
                                   'percent_credit_score_over_700',
                                   'percent_own_current_home',
                                   'percent_flexible_move_in_date',
                                   'percent_long_term_lease',
                                   'percent_more_than_one_bed',
                                   'percent_need_parking',
                                   'num_contacts_per_rental',
                                   'zindex'])):

    __slots__ = ()

    def new(cls,
            region_id,
            median_monthly_income,
            mean_house_hold_size,
            mean_min_bed,
            mean_max_bed,
            percent_credit_score_over_700,
            percent_own_current_home,
            percent_flexible_move_in_date,
            percent_long_term_lease,
            percent_more_than_one_bed,
            percent_need_parking,
            num_contacts_per_rental,
            zindex):
        return super(NeighborhoodData, cls).__new__(cls,
                                                    region_id,
                                                    median_monthly_income,
                                                    mean_house_hold_size,
                                                    mean_min_bed,
                                                    mean_max_bed,
                                                    percent_credit_score_over_700,
                                                    percent_own_current_home,
                                                    percent_flexible_move_in_date,
                                                    percent_long_term_lease,
                                                    percent_more_than_one_bed,
                                                    percent_need_parking,
                                                    num_contacts_per_rental,
                                                    zindex)

def _create_neighborhood_data_from_sql(neighborhood_data):
    return NeighborhoodData(
        region_id=
            int(neighborhood_data['RegionId']),
        median_monthly_income=
            float(neighborhood_data['MedianMonthlyIncome']),
        mean_house_hold_size=
            float(neighborhood_data['MeanHouseHoldSize']),
        mean_min_bed=
            float(neighborhood_data['MeanMinBed']),
        mean_max_bed=
            float(neighborhood_data['MeanMaxBed']),
        percent_credit_score_over_700=
            float(neighborhood_data['PercentCreditScoreOver700']),
        percent_own_current_home=
            float(neighborhood_data['PercentOwnCurrentHome']),
        percent_flexible_move_in_date=
            float(neighborhood_data['PercentFlexibleMoveInDate']),
        percent_long_term_lease=
            float(neighborhood_data['PercentLongTermLease']),
        percent_more_than_one_bed=
            float(neighborhood_data['PercentMoreThanOneBed']),
        percent_need_parking=
            float(neighborhood_data['PercentNeedParking']),
        num_contacts_per_rental=
            float(neighborhood_data['NumContactsPerRental']),
        zindex=
            float(neighborhood_data['Zindex'])
   ) 
@DBTransaction('user_db')
def get_neighborhood_data_by_region_id_neighborhood(region_id_neighborhood,
                                                    session=None):
    """Get aggregate renter data in a neighborhood"""
    query = ('exec dbo.NeighborhoodDataGetByRegionIDNeighborhood'
             ' :region_id_neighborhood')
    params = dict(region_id_neighborhood=region_id_neighborhood)
    result = session.execute(query, params).fetchone()
    return _create_neighborhood_data_from_sql(result)._asdict() if result else None
