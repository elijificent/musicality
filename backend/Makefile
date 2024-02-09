.PHONY: test
test:
	python -m unittest tests/test_*.py

install-requirements:
	pip install -r requirements.txt

save-requirements:
	pip freeze > requirements.txt

format:
	black src

twinkles:
	python -m src.musicxml.notes

.PHONY: clean
clean:
	rm sample_files/twinkles/*.musicxml