
# Save typing lengthy command lines for i18n

default:
	@echo "Makefile is used for i18n"
	@echo ""
	@echo "'make extract' update all the .pot and .po files"
	@echo "'make install' compile .po files"

MSGS = "messages.pot"

ATD = "."

extract: pot fr

install:
	pybabel compile -d $(ATD)

pot:
	pybabel extract -F babel.cfg -k tr -o $(MSGS) ..

fr:
	mkdir -p $(ATD)/fr/LC_MESSAGES
	touch $(ATD)/fr/LC_MESSAGES/messages.po
	pybabel update -i $(MSGS) -d $(ATD) -l fr

