all:
	python3 gpxActivities.py
	open website/index.html
strava:
	python3 stravaActivities.py
	open website/index.html
example:
	python3 gpxActivities.py < sampleInput
	open website/index.html
clean:
	rm website/*
