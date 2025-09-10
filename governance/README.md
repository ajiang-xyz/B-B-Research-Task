# Governance

To produce Figures 1 and 2 in my submission:
1. `pip install -r requirements.txt`
2. `python scaling_visualizations.txt`

To scrape the addresses that voted on Proposal 289:
1. Open `prop289_voters_scraper.js` in a text editor and follow the directions at the top.

To verify my claims about the 14 suspicious wallets, query the Block's Compound governance subgraph:
1. Create an API key at https://thegraph.com/studio/apikeys/
2. `THEGRAPH_API_KEY=<your_api_key_here> node historical_votes_scraper.js`
