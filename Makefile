.PHONY: heatmap
heatmap:
	python -m mc_map_generator heat-map Station_list.csv

.PHONY: setup
setup:
	pip install -r requirements.txt
