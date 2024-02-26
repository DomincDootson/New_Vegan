from datetime import datetime
from Parsing_Functions import image_filepath

class Recipe():
	
	def __init__(self, address):
		self.read_recipe_card(address)

	## Datetime formatting ##
	## ------------------- ## 

	def convert_str_2_datetime(self):
		self.date = datetime.strptime(self.date, '%a %d %b %Y %H.%M %Z')	

	def string_from_datetime(self):
		return datetime.strftime(self.date, '%a %d %b %Y %H.%M %Z') + "GMT"

	## Recipe Card Reading & Writing ##
	## ----------------------------- ##

	def read_recipe_card(self, file_path):
		with open(file_path, 'r') as f:
			self.read_title(f)
			self.read_preamble(f)
			self.read_date(f)
			line = self.read_info(f)
			self.read_ingredients(f, line)
			self.read_steps(f)
			f.close()

	def read_title(self, file):
		self.title = file.readline().replace('\n', "")
		print(self.title)
		file.readline()

	def read_preamble(self, file):
		line, self.preamble = file.readline(), ""
		while line != '\n':
			self.preamble += line
			line = file.readline()
		self.preamble = self.preamble[:-1]

	def read_date(self, file):
		self.date = file.readline().replace('\n', "")
		self.convert_str_2_datetime()
		file.readline()

	def read_info(self, file):
		self.initialise_info()
		line = file.readline()
		if not ':' in line:
			return line

		while line != '\n' or (':' in line): # We need the second conditional for those recipes that don't have info
			position_of_colon = line.find(':')
			self.info[line[:position_of_colon]] = line[position_of_colon+2:].replace('\n', "")

			line = file.readline()
		
		return file.readline()

	def read_ingredients(self, file, line):
		self.ingredients = []

		while line != "Steps\n":
			sub_list = []
			while line != '\n':
				sub_list.append(line.replace('\n',""))
				line = file.readline()
			
			(self.ingredients).append(sub_list)
			line = file.readline()

	def read_steps(self, file):
		self.steps, line = [], file.readline()
		while line[-1] == '\n':
			(self.steps).append(line)
			line = file.readline()
			if len(line) == 0:
				break # if a final line is added at the end of the recipe
			
		(self.steps).append(line)

		self.steps = [step.replace('\n',"") for step in self.steps]


	## Recipe tex String ##
	## ----------------- ##

	def get_recipe_tex_string(self, include_fig = True):
		tex_string = self.get_tex_title()

		if include_fig:
			tex_string += self.get_tex_image()

		tex_string += self.get_tex_preamble() + self.get_tex_info() + self.get_tex_ingredients() + self.get_tex_steps() + "\\newpage\n\n"
		return tex_string

	def get_tex_title(self):
		return f"\\section{{{self.title}}}\n" 


	def get_tex_image(self):
		string = "\\begin{figure}\n"
		string += "\\centering"
		string += rf"\includegraphics[width=10cm,height=10cm,keepaspectratio]{{{image_filepath(self.title)}}}" + '\n'
		string += "\end{figure}\n"
		return string

	def get_tex_preamble(self):
		string = self.preamble.replace('\n', '\\\\ \n')
		return f"\\emph{{{string}}}\\\\\\\\ \n"

	def get_tex_info(self):
		string = ""
		for key in self.info:
			if self.info[key] != None:
				string += f"\\textbf{{{key}}}: " + self.info[key] +'\n' # Use {{}} (double) in f string to output single {}
		return string

	def get_tex_ingredients(self):
		string = "\\subsection*{Ingredients}\n"
		for subset in self.ingredients:
			string += "\\begin{itemize}\n"
			for ingredient in subset:
				string += f"\\item {ingredient}\n"
			string += "\\end{itemize}\n\n"

		return self.replace_unicode_with_tex(string)


	def get_tex_steps(self):
		"\\subsection*{Steps}"
		string = "\\subsection*{Steps}\n\\begin{enumerate}\n"
		for step in self.steps:
			if len(step) != 0:
				string += f"\\item {step}\n"

		string += "\\end{enumerate}\n"
		return self.replace_unicode_with_tex(string)

	def replace_unicode_with_tex(self, string): # there are some characters that latex doesn't like this, replace them with things it does like
		to_replace = {"½" : r"$\frac{1}{4}$", 
		"¼" : r"$\frac{1}{4}$", "¾" : r"$\frac{3}{4}$", 
		"⅓" : r"$\frac{1}{3}$", "⅔" : r"$\frac{2}{3}$", 
		"⅛" : r"$\frac{1}{8}$",
		"%" : r"\%"}
		

		for key in to_replace:
			if key in string:
				string =string.replace(key, to_replace[key])
		
		return string