# Route Similarity Visualizer

This project provides tools to parse cycling routes from `.gpx` files or Strava activities, compute similarity between routes using k-minhash based Jaccard similarity estimation, and visualize the results in interactive HTML maps.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Directory Structure](#directory-structure)  
- [Makefile Explanation](#makefile-explanation)  
- [Setup and Requirements](#setup-and-requirements)  
- [Strava OAuth Authorization](#strava-oauth-authorization)  
- [`.token` File Format](#token-file-format)  
- [Usage Instructions](#usage-instructions)  
- [Module and Function Documentation](#module-and-function-documentation)  

---

## Project Overview

- **gpxActivities.py**: Load `.gpx` files from the `data` directory, let user select one route, and plot the top K most similar routes.
- **stravaActivities.py**: Fetch recent Strava activities using Strava API and OAuth, allow user to select a route, then plot the top K most similar routes.
- **transfer.py** and **parselatlon.py**: Core modules that implement GPX parsing, coordinate transformations, k-minhash similarity calculations, and route visualization.
- **exampleWebsite/index.html**: Pre-built example output for user reference.

---

## Directory Structure

```

/
├── data/                  # Place your .gpx files here for gpxActivities.py
├── exampleWebsite/        # Contains example HTML output
│   └── index.html
├── website/               # Generated HTML visualizations are output here
├── gpxActivities.py
├── stravaActivities.py
├── transfer.py
├── parselatlon.py
├── kminhash.py
├── Makefile
├── .token                 # Stores Strava API credentials (client\_id, client\_secret, refresh\_token)
├── sampleInput            # Sample input file for example Makefile usage
└── README.md

````

---

## Makefile Explanation

The `Makefile` helps automate running scripts and cleaning output files. It contains the following targets:

- `all`  
  Runs `gpxActivities.py` to process `.gpx` files in `data/` and opens `website/index.html` in your browser.

- `strava`  
  Runs `stravaActivities.py` to fetch routes from Strava and then open `website/index.html`.

- `example`  
  Runs `gpxActivities.py` with `sampleInput` as input (useful for demo/testing), then opens `website/index.html`.

- `clean`  
  Removes all generated files inside the `website/` directory to clean up.

---

## Setup and Requirements

### Python Dependencies

Install required packages using:

```bash
pip install -r requirements.txt
````

**requirements.txt**

```
requests
urllib3
pandas
numpy
matplotlib
folium
polyline
tqdm
```

---

## Strava OAuth Authorization

To use `stravaActivities.py`, you must authorize your app with Strava:

1. Create a Strava API app on [https://developers.strava.com/](https://developers.strava.com/)
2. Put your `client_id`, `client_secret`, and a `refresh_token` in a `.token` file (see below).
3. Run `stravaActivities.py`, which will print an authorization URL.
4. Open the URL, log in, and authorize the app.
5. After redirection, copy the URL you were redirected to and paste it into the script prompt.
6. The script exchanges the code for an access token and downloads your recent activities.

---

## `.token` File Format

The `.token` file must contain exactly three lines, each storing:

```
client_id
client_secret
refresh_token
```

No extra whitespace or empty lines.

---

## Usage Instructions

### Using GPX files

1. Place all your `.gpx` files inside the `data/` directory.
2. Run

```bash
make all
```

3. The script lists all `.gpx` files and asks for the index of the reference route and how many similar routes to visualize.
4. The visualization will open automatically in your default browser.

### Using Strava activities

1. Prepare `.token` file as described above.
2. Run

```bash
make strava
```

3. Follow the OAuth instructions to authorize and provide the redirected URL.
4. Choose route index and number of similar routes to plot.
5. Results open automatically in the browser.

### Example run with sample input

```bash
make example
```

---

## Module and Function Documentation

### parselatlon.py

* `parseGpx(fileName)`
  Parses a `.gpx` file and returns a list of `(lat, lon)` tuples.

* `trans(latlon)`
  Converts `(lat, lon)` coordinates into Global Grid cell indices.

### kminhash.py

* `evaluate(K, point, P)`
  Computes the smallest K polynomial hash values from the input points.

### transfer.py

* `paint(coordinate1, coordinate2, p, path)`
  Draws two routes and their similarity score to an output file.

* `getmin(coordinate, P)`
  Returns the K-minhash array of coordinates.

* `evaluate(coordinatea, coordinateb, P)`
  Estimates Jaccard similarity between two coordinate sets.

* `evaluateraw(coordinate1, coordinate2)`
  Estimates similarity directly from raw GPS coordinates.

* `evaluatepath(path1, path2, path)`
  Computes similarity between two `.gpx` routes and saves visualization.

* `sortpath(coors, index, K)`
  Finds the top K most similar routes to a target route by index.

* `paintpath(coors, index, K)`
  Generates an HTML visualization for the top K similar routes.

