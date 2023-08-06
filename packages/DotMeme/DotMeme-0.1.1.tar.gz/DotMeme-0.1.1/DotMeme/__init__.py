import yaml
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import zipfile
import os


def meme(memeFilePath, *points, imageName="meme.png", saveMeme=False):
	"""
	Function that reads a .meme file and create a meme from it with the text specified
	:param memeFilePath:
		The name of the meme or path
	:param points:
		The text for the points
	:param imageName:
		The output name of the image if it to be saved. default is meme.png
	:param saveMeme:
		Boolean, to save the meme to a file or not. default is False
	:return:
		Returns the Pillow img object
	"""
	# Checks if the person has .meme on the file specified
	if '.meme' in os.path.basename(memeFilePath) is False:
		memeFileName = os.path.basename(memeFilePath) + '.meme'
	else:
		memeFileName = os.path.basename(memeFilePath)

	# Checks if the file exists and if it doesn't then it chcks if the package has it
	try:
		open(memeFilePath)
	except FileNotFoundError:
		memeFilePath = os.path.join(__path__[0],'Data', 'Memes', memeFileName)
	try:
		with open(memeFilePath) as f:
			ymlData = yaml.safe_load(f)
			response = requests.get(ymlData['image']['url'])
			img = Image.open(BytesIO(response.content))

	# This means that it is a zip file
	except UnicodeDecodeError:
		archive = zipfile.ZipFile(memeFilePath, 'r')
		ymlData = archive.read(memeFileName).decode('utf-8')
		ymlData = yaml.safe_load(ymlData)
		for file in archive.namelist():
			if ".jpg" in file or ".png" in file:
				img = Image.open(archive.open(file))
				break
	except FileNotFoundError:
		exit
		raise Exception("MemeNotFoundError")


	# Checks that the correct number of points are added
	assert len(points) == len(ymlData['text']), f"Incorrect number of points, you have entered text for {len(points)} but it requires {len(ymlData['text'])}"
	draw = ImageDraw.Draw(img)
	pointIndex = 0
	# Places the text onto the image for each point
	for point in ymlData['text']:
		point1, point2 = ymlData['text'][point]['point'].split()
		# Convert the points from string to int for the position
		point1 = int(point1)
		point2 = int(point2)
		text = points[pointIndex]
		textPosition = (point1, point2)
		fontLocation = os.path.join(__path__[0], 'Data', 'font.ttf')
		font = ImageFont.truetype(fontLocation, size=45)
		draw.text(textPosition, text, (0, 0, 0), font=font)
		pointIndex += 1
	if saveMeme:
		img.save(imageName, optimize=True)
	return img

def listMemes():
	"""
	A generator that yields all the memes that the package has
	:return:
		yields the meme files with .meme extension
	"""
	os.chdir(os.path.join(__path__[0], 'Data', 'Memes'))
	for meme in os.listdir():
		yield meme
