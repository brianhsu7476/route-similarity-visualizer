all:
	python3 gpxActivities.py
strava:
	python3 stravaActivities.py
example:
	python3 gpxActivities.py < sampleInput
clean:
	rm website/*
