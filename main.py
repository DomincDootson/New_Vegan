from src.RecipeScrapper import get_recipe, get_all_recipes
from src.Recipe import Recipe
if __name__ == "__main__":
	

	get_all_recipes() # Gets all the recipes

	recipe_book = Recipe_Book() # Create the cook book object
	recipe_book.save_tex_cookbook() # Saves all the recipes to file 