from bs4 import BeautifulSoup
import shutil
import requests
import src.Parsing_Functions 
PAGES_2_IGNORE = {'weekly-meal-plan', 'https://www.theguardian.com/lifeandstyle/2018/jan/27/meera-sodhas-vegan-swede-laksa-recipe'}
INFO_KEYWORDS = {"Prep", "Cook", "Chill", "Rest", "Soak", "Proving", "Freeze", "Serves", "Makes", 'Prove'}

## Parsing Functions ##
## ----------------- ##

def get_date(soup):
	''' Gets the date from the website'''
	date = 0
	if soup.find('summary', class_ = 'dcr-12fpzem') is not None:
		date = (soup.find('summary', class_ = 'dcr-12fpzem').text)
		
	elif (soup.find('div', class_ = 'dcr-km9fgb') is not None):	
		date = (soup.find('div', class_ = 'dcr-km9fgb').text)
	elif (soup.find('div', class_ = 'dcr-1d52k2r') is not None):	
		
		date = (soup.find('div', class_ = 'dcr-1d52k2r').text)

	return date

def get_body(soup) -> str:
	'''This function gets all the recipe informnation and returns it correctly formatted for the recipe card'''
	body_html = soup.find_all('p', class_ = 'dcr-170x4j1') # Get all the text in the right tag

	preamble,body_html = get_preamble(body_html)
	info, body_html = get_info(body_html)
	ingredients, steps = get_ingredients_and_steps(body_html)
	
	return preamble, info, ingredients, steps

def get_preamble(body_html):
	'''Will take a soup object and return the correctly formatted preamble and the html with preamble removed'''
	preamble_lst = []
	count = 0
	for s_tag in body_html:
		
		if not contains_strong_tag(s_tag):
			count +=1
			preamble_lst.append(s_tag.text)
		else:
			return format_preamble(preamble_lst), body_html[count:]
	

def get_info(body_html) -> str:
	'''This function will scrape all the information '''
	info = {}	
	
	text = body_html[0].text
	positions_of_key_words = []

	for key in INFO_KEYWORDS:
		positions_of_key_words.append(text.find(key))

	positions_of_key_words.sort()
	positions_of_key_words = [x for x in positions_of_key_words if x >= 0]

	for i in range(len(positions_of_key_words)):
		if (positions_of_key_words[i] != positions_of_key_words[-1]):
			positions_of_key_words[i] = [positions_of_key_words[i], positions_of_key_words[i+1]]

		else:
			positions_of_key_words[-1] = [positions_of_key_words[-1], len(text)]


	for pair in positions_of_key_words:
		for key in INFO_KEYWORDS:
			if key in text[pair[0]:pair[1]]:
				info[key] = text[pair[0]:pair[1]].replace(key, "").strip()
		
	return format_info(info), body_html[1:]

def get_ingredients_and_steps(soups) -> str: 
	''' Splits the ingredients and steps out. It would be hard to split due to the regex'''
	ingredients, steps = [], []
	for soup in soups:
		if "<strong>" in str(soup): # Each group of ingredience will contain a <strong> tag
			strings = str(soup).split("<br/>")
			ingredients.append([remove_html_tags(string) for string in strings][:])
		else:
			steps.append(remove_html_tags(str(soup)))

	return format_ingredients(ingredients), format_steps(steps)


## Formatting Functions ##
## -------------------- ##
def format_preamble(preamble_2_format :list[str]) -> str:
	return '\n'.join(preamble_2_format) + '\n\n'

def format_info(info_2_format : dict[str, str]) -> str:
	formatted_info = ""
	if len(info_2_format)!=0: # TODO WRITE THIS FUNCTION, HAVE WE OVERCOMPLICATED IT?
		for key in info_2_format:
			if info_2_format != None:
				formatted_info += f"{key} : {info_2_format[key]}" + '\n'
		formatted_info +='\n'
	return formatted_info
	
	

def format_ingredients(ingredients_2_format : list[str]) -> str: # TODO: this can be tidyied
	if len(ingredients_2_format) == 1: 
		return '\n'.join(ingredients_2_format[0]) + "\n\n"
	else:
		return '\n\n'.join(['\n'.join(part) for part in ingredients_2_format]) +"\n\n"
		

def format_steps(steps_2_format : list[str]) -> str:
	return "Steps\n" +'\n'.join(steps_2_format)

## Image Function ##
## -------------- ##
def image_filepath(title) -> str:
	''' Returns the filepath of where the image should be saved '''
	string = "Recipe_Pictures/" +title.replace(" ", "_") + ".png"
	string = string.replace("'", '')
	return string.replace('"','')


def get_image(soup, image_filepath) -> None:
	''' Saves the image'''
	image_url = soup.find('img')['src'] # I deleted this to make it work dcr-1989ovb
	print(image_url)
	
	r = requests.get(image_url, stream = True)
	r.raw.decode_content = True
	with open(image_filepath,'wb') as f:
		shutil.copyfileobj(r.raw, f)


## Utility Functions ##
## ----------------- ## 

def if_bad_web_adress(web_address : str) -> bool:
	''' Will return true if the web address contrains a substring contained in PAGES_2_IGNORE '''
	return any(sub_string in web_address for sub_string in PAGES_2_IGNORE)

def remove_html_tags(string : str) -> str:
	''' Removes any html'''
	split_string, string =  [char for char in string], '' # you don't need to split it 
	is_in_tag = False

	for char in split_string:
	
		if (char == '<' or is_in_tag):
			is_in_tag = True 
			if char == '>':
				is_in_tag = False
		else:
			string += char

	return string

def contains_strong_tag(soup_tag) -> bool:
	''' Will return True if a tag contains a strong element, this will be used in REGEX'''
	return True if soup_tag.find('strong') is not None else False
		