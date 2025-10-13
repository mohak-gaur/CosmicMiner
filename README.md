# CosmicMinerBot (scaffold)

This project scaffold implements a modular Page Object Model (POM) for your Cosmic Miner automation.

Structure:
- config.py: configuration constants
- core/: driver and excel helpers, business logic
- pages/: selenium page objects
- workflows/: higher-level flows using page objects
- utils/: helpers and logging
- main.py: sample entrypoint that builds hierarchy and writes referral_results.xlsx

Notes:
- You need Chrome + chromedriver. The project uses `webdriver_manager` to fetch driver.
- Fill `Cosmic Miner/users.xlsx` before running.
- To run quick check without opening visible browser, main.py uses headless mode in hierarchy builder.
