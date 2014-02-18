SOURCE_PATH=.
BACK_PATH=./pdf/back

all: compile move


compile:
	pdflatex $(SOURCE_PATH)/gettingStarted.tex
	rm *.aux *.log 

move:
	- mkdir -p $(BACK_PATH)
	- mv pdf/*.pdf $(BACK_PATH)
	- mv *.pdf pdf/

clear:
	- rm -r pdf/
