# New Vegan Cookbook

## Overview 

This is a little project I gave myself to learn how to webscrape using the 'BeautifulSoup' library for python. My plan was to take all the recipes on the Guardian's new vegan blog and convert it into a pdf sorted by the month in which they were published. It worked pretty well: I learnt how to use BeautifulSoup and the fiddly nature of webscrapping - there will always be expections to deal with! There also seem to be some pretty great recipies as well. 

I should highlight that none of the recipies in this are my own work, they where all taken from The Guardian's blog called "The New Vegan" (https://www.theguardian.com/food/series/the-new-vegan). 

## Code Overview 
All the code is contained in the src file is run via main.py. The code does two different jobs and is organised as:

- **Recipe Scrapping and Saving to File.**
	- `Parsing_Functions.py`: A collection of functions that take a soup object and correctly formats the different parts of the recipes. Also has functions for cleaning them into the correct format for the recipe cards (an example, Caramelised onion ramen, is saved in this file).
	- `Recipe_Scrapper.py': This is the main writing function for the recipe cards. It generates all the URLS and then, for each recipe, collects the different parts and writes them to file as .txt files. Note, it might have made more sense to save them as .tex and then just read that itm rather than internet -> .txt -> .tex, but oh well. 
	
- **Recipe Book Creation**
	- `Recipe.py` reads in a recipe and stores each part of the recipe as different memeber variable. It has memeber functions that can produce a string that is the tex for that recipe card.
	- `RecipeBook.py' a container class that holds all the recipes and has memeber functions that to create the cookbook

Once the .tex is created then, it can be rendered with your latex renderer of choice. 

I have decide not to leave the recipe cards and the pdf in the git (apart from the example) as I would like to not get sued. I have also include some screenshots of the pdf to illustrate its design (some call in 'normcore' some call it arXiv chic...)

Please note, I have nothing against those that only eat rabbit food, but I am not a rabbit myself. I just really 
like these recipes. 
