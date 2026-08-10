.PHONY: profile test validate all
profile:
	python3 scripts/profile_engine.py --offline

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_profile.py

all: profile test validate
