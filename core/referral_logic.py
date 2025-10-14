from collections import deque
from copy import deepcopy
from config import PLAN_AMOUNT_MAP

def determine_rank(user, direct_miners, referral_map):
    if user['DirectMiners'] < 15 or user['IndirectMiners'] < 250:
        return None
    child_ranks = [
        referral_map[child['MyReferral']]['Rank']
        for child in direct_miners
        if referral_map.get(child['MyReferral']) and referral_map[child['MyReferral']]['Rank']
    ]
    if child_ranks.count('Elite') >= 3:
        return 'Quantum'
    elif child_ranks.count('Pro') >= 3:
        return 'Elite'
    elif child_ranks.count('Basic') >= 3:
        return 'Pro'
    else:
        return 'Basic'

def valid_split(business_shares):
    if len(business_shares) < 3:
        return False
    top_three = sorted(business_shares, reverse=True)[:3]
    t1, t2, t3 = [round(x, 2) for x in top_three]
    return t1 == 40.0 and t2 == 30.0 and t3 == 30.0

def determine_star_rank(user, direct_miners, referral_map):
    # Applies only to paid users
    if not user.get('PlanID'):
        return 1
    total_business = user.get('TotalBusiness', 0)
    if user['DirectMiners'] < 15 or user['IndirectMiners'] < 250 or total_business < 10000:
        return 1
    shares = []
    for child in direct_miners:
        cu = referral_map.get(child['MyReferral'])
        if cu and cu['TotalBusiness'] > 0:
            share_percent = (cu['TotalBusiness'] / total_business) * 100
            shares.append(share_percent)
    if not valid_split(shares):
        return 1
    child_stars = [
        referral_map[child['MyReferral']]['StarRank']
        for child in direct_miners
        if referral_map.get(child['MyReferral']) and referral_map[child['MyReferral']]['StarRank']
    ]
    for star_level in range(7, 1, -1):
        required = star_level - 1
        if child_stars.count(required) >= 3:
            if valid_split(shares):
                return star_level
    return 2

def calculate_metrics(referral_map, user_ref, visited=None):
    if visited is None:
        visited = set()

    # Prevent infinite recursion
    if user_ref in visited:
        return 0, 0
    visited.add(user_ref)

    user = referral_map[user_ref]
    # Get direct miners for this user
    direct_miners = [
        child for child in referral_map.values()
        if child['ParentReferral'] == user_ref
    ]
    user['DirectMiners'] = len(direct_miners)

    indirect_miners = 0
    total_business = 0

    # Include own plan amount
    if user.get('PlanID'):
        # plan_id = int(user['PlanID'])
        total_business += PLAN_AMOUNT_MAP.get(user['PlanID'], 0)

    # Recursively calculate for children
    for child in direct_miners:
        im, tb = calculate_metrics(referral_map, child['MyReferral'], visited)
        indirect_miners += 1 + im
        total_business += tb

    user['IndirectMiners'] = indirect_miners
    user['TotalBusiness'] = total_business

    # Determine Rank (applies to all)
    user['Rank'] = determine_rank(user, direct_miners, referral_map)

    # Determine Star (only for paid users)
    user['StarRank'] = determine_star_rank(user, direct_miners, referral_map)

    return indirect_miners, total_business


def build_referral_map_from_results(results, start_referral):
    # results: list of tuples (user, parent, new_ref, level, plan_id)
    referral_map = {}
    for (user, parent, new_ref, lvl, plan) in results:
        entry = deepcopy(user)
        entry.update({
            'ParentReferral': parent,
            'MyReferral': new_ref,
            'Level': lvl,
            'PlanID': plan,
            'DirectMiners': 0,
            'IndirectMiners': 0,
            'TotalBusiness': 0,
            'Rank': None,
            'StarRank': 1
        })
        referral_map[new_ref] = entry
    # add root if missing
    if start_referral not in referral_map:
        referral_map[start_referral] = {
            'Name': 'Root',
            'Email': '',
            'ParentReferral': None,
            'MyReferral': start_referral,
            'Level': 0,
            'PlanID': None,
            'DirectMiners': 0,
            'IndirectMiners': 0,
            'TotalBusiness': 0,
            'Rank': None,
            'StarRank': 1
        }
    return referral_map
