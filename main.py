import logging
from utils.logger import setup_logging
from core.excel_utils import read_users, write_results
from workflows.hierarchy_builder import build_hierarchy
from core.referral_logic import build_referral_map_from_results, calculate_metrics
import config
import pandas as pd

def main():
    setup_logging()
    users = read_users(config.EXCEL_FILE, config.EXCEL_SHEET)
    results = build_hierarchy(users, config.START_REFERRAL_CODE, children_per_parent=config.CHILDREN_PER_PARENT, max_levels=config.MAX_LEVELS, headless=True)
    referral_map = build_referral_map_from_results(results, config.START_REFERRAL_CODE)
    calculate_metrics(referral_map, config.START_REFERRAL_CODE)

    # prepare DataFrame
    rows = []
    for ref, u in referral_map.items():
        if ref == config.START_REFERRAL_CODE:
            continue
        rows.append({
            'Name': u.get('Name'),
            'Email': u.get('Email'),
            'ParentReferral': u.get('ParentReferral'),
            'MyReferral': ref,
            'Level': u.get('Level'),
            'PlanID': u.get('PlanID'),
            'DirectMiners': u.get('DirectMiners'),
            'IndirectMiners': u.get('IndirectMiners'),
            'TotalBusiness': u.get('TotalBusiness'),
            'Rank': u.get('Rank') or '-',
            'StarRank': f"{u.get('StarRank')}★" if u.get('PlanID') else 'N/A',
            'CombinedRank': f"{u.get('Rank') or '-'} | {u.get('StarRank')}★" if u.get('PlanID') else f"{u.get('Rank') or '-'} | Free"
        })
    df = pd.DataFrame(rows)
    write_results(df, path='referral_results.xlsx')
    logging.info('Saved referral_results.xlsx')

if __name__ == '__main__':
    main()
