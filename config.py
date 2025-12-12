# Configuration file for CosmicMinerBot
EXCEL_FILE = r'C:\CosmicMiner\users1.xlsx'
EXCEL_SHEET = 'users'

# START_REFERRAL_CODE = 'QM1JEHOY'
START_REFERRAL_CODE = 'X2IZ9M7C' #paid_cosmic_main
CHILDREN_PER_PARENT = 2
MAX_LEVELS = 2
# ADMIN_USERNAME = "Admin"
# ADMIN_PASSWORD = "123456"
ADMIN_USERNAME = "cosmipower"
ADMIN_PASSWORD = "bgHxQ4MkrziTpbq"
ADMIN_URL = "https://cosmiminer.in/owebest/website/admin/login.php"

REGISTER_URL = "https://cosmiminer.in/owebest/website/register.html"
SITE_HOME_URL = "https://cosmiminer.in/owebest/website/index.html"


# 1 -> Basic Miner
# 2 -> Pro Miner
# 3 -> Elite Miner
# 4 -> Quantum Miner
plan_id = 1

PLAN_MAP = {
    1: {
        "name": "Basic Miner",
        "onclick_fragment": "plan_id=1",
        "default_amount": 35,    # corresponds to '30.000 USDT' bucket
    },
    2: {
        "name": "Pro Miner",
        "onclick_fragment": "plan_id=2",
        "default_amount": 110,   # corresponds to '101.000 USDT' bucket
    },
    3: {
        "name": "Elite Miner",
        "onclick_fragment": "plan_id=3",
        "default_amount": 252,   # corresponds to '251.000 USDT' bucket
    },
    4: {
        "name": "Quantum Miner",
        "onclick_fragment": "plan_id=4",
        "default_amount": 1002,  # corresponds to '1001.000 USDT' bucket
    }
}

# PLAN_AMOUNT_MAP = {
#     1: 80,
#     2: 200,
#     3: 800,
#     4: 4500
# }