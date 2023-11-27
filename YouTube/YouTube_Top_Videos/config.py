#config.py
api_key = 'insert your api key...see links on README.md'
search_query = 'BUN KEBAB RECIPES'
max_results = 1000000
top = 5
final_cols = ['SNo', 'Video Title', 'Views', 'Likes','Video Link', 'Channel Title', 'Channel Link', 'Subscribers', 'Channel Views', 'Total Videos']
int_cols = ['Views', 'Likes', 'Channel Views', 'Total Videos']
sorting_cols = ['Likes', 'Views']
sorting_order = [False, False] # False will sort in Descending Order and number of list elements must be equal to those in sorting_cols
