-Data sources used, including instructions for a user to access the data sources
I used Reddit and Wikipedia as my data sources. For Reddit, you do need a key to access the data, which I attached in the secrets.py file; Wikipedia do not need API key, but instead need to install "wikipedia" package on python.



-Any other information needed to run the program (e.g., pointer to getting started info for plotly)
None.


-Brief description of how your code is structured, including the names of significant data
processing functions (just the 2-3 most important functions--not a complete list) and
class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
I first caching the data from both site, and collecting the data into database. 
Function that I use for processing data: get_reddit_data/ get_wiki_data/ reddit_post



-Brief user guide, including how to run the program and how to choose presentation
options
this program is run on command line. After running the program, you can type help to see the 5 options: Summary/ country/ graph/ reddit/ exit. So for the summary option, you can read the introduction of "the four asian tigers"; and if you want to learn more about specific one country, you can type in 'country' and then type in the 'country name' to read the introduction for that country. For graph, you will have either 'bar plot' and 'map' option to choose; 'bar plot' will visualize the population for the countries, and 'map' will give you demographic image for the countries. From 'Reddit', you can see within each country category,  what is the top ten trendy post, including author, post url. 'Exit' text the program. All command lines should be written lowercase.# SI507_final_project
