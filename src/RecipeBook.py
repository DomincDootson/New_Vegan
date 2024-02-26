from bs4 import BeautifulSoup
import shutil
import requests

from Recipe import Recipe 

class RecipeBook():
	def __init__(self, file_path_for_Index = "Recipe_Cards/Index.txt"):
		'''Takes the file location of an index card, contain the recipes that we want to read in'''
		self.recipes = []
		with open(file_path_for_Index, 'r') as f:
			file = f.readline().replace('\n', "")
			
			while file !="":
				self.recipes.append(Recipe(file, False))
				file = f.readline().replace('\n',"")
				
			f.close()

	def list_of_recipies(self):
		[print(recipe.title) for recipe in self.recipes]
		print(len(self.recipes))
		

	## Methods to Create tex file ##
	## -------------------------- ##

	def save_tex_cookbook(self, file_name = "New_Vegan_Cookbook.tex"):
		''' Saves the cookbook as a tex file'''
		self.read_recipes_from_file()
		string =""
		recipe_book.sort_by_month()
		with open(file_name, 'w') as f:
			f.writelines(self.read_in_tex_preamble())
			f.writelines(self.generate_recipes_tex())
			f.writelines("\\end{document}")
			f.close()

	def read_in_tex_preamble(self, preamble_file = "tex_preamble.tex"):
		'''Reads in the preamble for the cookbook''' 
		string = ""

		with open(preamble_file, 'r') as f:
			line = f.readline()
			while ("\\mainmatter" not in line):
				string += line
				line = f.readline()
		return string + "\\mainmatter\n"

	def generate_recipes_tex(self):
		string, month = "\\chapter{January}\n", 1
		for recipe in self.recipes:
			if recipe.date.month != month:
				month = recipe.date.month
				string += f"\\chapter{{{recipe.date.strftime('%B')}}}\n"

			string += recipe.get_recipe_tex_string()
		return string


	## Misc functions ##
	## -------------- ##	
	def sort_by_month(self):
		self.recipes.sort(key = lambda x: x.date.month)
				