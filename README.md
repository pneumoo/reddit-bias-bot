# (2017) reddit-bias-bot

This is an archived set of tools I made in 2017 to try to combat mis/disinformation and poor quality news on reddit. These files haven't been updated since then, so this upload to GH is an archival step. 

###Contents: 
* Data for bias was gathered from AllSides.com and MediaBiasFactCheck.com using the scraper scripts allsidesscrape.py and the pair mbfcpagesscrape.py and mbfcscrape.py. 
* This data was then used by some reddit bots to take action on reddit submissions. 

submission_source_uvdv_bot.py and subreddit_rising_uvdv_bot.py would upvote or downvote submissions based on the "neutralness" of the source. Fake, conspiracy, and extreme (right and left) sources were downvoted. Center-left/right and Neutral sources were upvoted. 

submission_bias_bot.py and submission_bias_bot2.py did not vote on the submission, but instead added a comment to the submission with details about the source's neutrality. The comment would include information linking back to AllSides.com or MediaBiasFactCheck.com so that users on reddit could be better informed. 
