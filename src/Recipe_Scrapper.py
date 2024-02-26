from bs4 import BeautifulSoup
import shutil
import requests
from src.Parsing_Functions import *

NEW_VEGAN_URL = "https://www.theguardian.com/food/series/the-new-vegan"

def get_all_recipes(page_url = NEW_VEGAN_URL, get_im = True):
	''' This function scrapes and saves all the recipes'''
	recipe_urls = scrape_recipes_from_page( True, page_url)
	for url in recipe_urls:
		get_recipe(page_url, get_im)



def scrape_recipes_from_page(first_page = True, page_url = NEW_VEGAN_URL, count =0):
	''' This gets the URLs for all the recipes'''
	source = requests.get(page_url).text
	soup = BeautifulSoup(source, "lxml")
	
	next_page_url = soup.find_all("a", class_ = "button button--small button--tertiary pagination__action--static")
	

	if len(next_page_url) == 1 and (not first_page):
		return []

	return [recipe['href'] for recipe in soup.find_all("a", class_ = "u-faux-block-link__overlay js-headline-text")]+scrape_recipes_from_page(first_page = False, page_url = next_page_url[-1]['href'], count = count+1)


def get_recipe(web_address : str, get_im : bool = True,  recipe_card_file : str = 'Recipe_Cards') -> None:
	''' This function will take a web address and save the recipe to file '''
	if if_bad_web_adress(web_address):
		return None 
	
	source = requests.get(web_address).text
	soup = BeautifulSoup(source, "lxml")
	title, date = soup.find('h2').text, get_date(soup)
	
	if get_im: 
		get_image(soup, image_filepath(title))


	write_recipe_2_file(title, date, *get_body(soup))
	

	

## Write to file ##
## ------------- ##

	
def write_recipe_2_file(title :str, date : str, preamble : str, info : str, ingredients : str, steps : str) -> None:
	file_path = 'test.txt' #get_recipe_name(title) 
	with open(file_path, 'w') as f:
		f.writelines(title+'\n\n')
		f.writelines(preamble)
		f.writelines(date+'\n\n')
		f.writelines(info)
		f.writelines(ingredients)
		f.writelines(steps)
		










	
	