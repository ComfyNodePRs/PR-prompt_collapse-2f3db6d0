fmt:
	isort prompt_collapse
	black prompt_collapse

test:
	pytest tests/


.PHONY: fmt test