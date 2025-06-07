---
title: README

---

# README

## 1. `parselatlon.py.parseGpx(fileName)`
- **Input**  
  - `fileName`: Name of the file to read; represents a `.gpx` file.
- **Output**  
  - An array representing all recorded points in the file, formatted as  
    `[(lat₁, lon₁), (lat₂, lon₂), ..., (latₙ, lonₙ)]`,  
    where each tuple is a latitude and longitude coordinate.
- **Sample Input**
    - `fileName`:`test.gpx`
- **Sample Output**
    - `[(25.0167050, 25.0167050), (l25.0167050, 121.9438760), ..., (21.9061360, 120.8506210)]`
---

## 2. `parselatlon.py.trans(latlon)`
- **Input**  
  - `latlon`: An array of length `N` containing latitude and longitude coordinates in the format  
    `[(lat₁, lon₁), (lat₂, lon₂), ..., (latₙ, lonₙ)]`.
- **Output**  
  - An array of converted Global Grid cell of level 20 indices, formatted as  
    `[(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)]`.
- **Sample Input**
    - `latlon`:`[(25.0167050, 25.0167050), (25.0167050, 121.9438760), ..., (21.9061360, 120.8506210)]`
- **Sample Output**
    - `[(150596, 145732), (150596, 710374), ..., (130840, 704005)]`
---

## 3. `kminhash.py.evaluate(K, point, P)`
- **Input**  
  - `K`: Number of minimum hash values to select.  
  - `point`: An array of integers to hash.  
  - `P`: A polynomial of degree `K-1` used for polynomial hashing.
- **Output**  
  - An array of length `K`, containing the smallest `K` hash results.
- **Sample Input**
    - `K`:3
    - `point`:`[1, 2, 3, 4, 5]`
    - `P`:`[1, 2, 3]`
- **Sample Output**
    - `[6, 17, 34]`
---

## 4. `transfer.py.paint(coordinate1, coordinate2, p, path)`
- **Input**  
  - `coordinate1`: An array of length `N₁` containing the latitude and longitude points of the first route.  
  - `coordinate2`: An array of length `N₂` containing the latitude and longitude points of the second route.  
  - `p`: The similarity score between the two routes.  
  - `path`: The output file path for the generated visualization.
- **Function**  
  - Draws both routes and the similarity score to the specified file.

---

## 5. `transfer.py.getmin(coordinate, P)`
- **Input**  
  - `coordinate`: An array of converted Global Grid cell of level 19 indices in the format  
    `[(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)]`.  
  - `P`: A polynomial of degree 100 (defined in `transfer.py`) used for hashing.
- **Output**  
  - An array of length `K = 100` representing the K-minhash results of the input coordinates.
- **Sample Input** (in this sample case,`K=5`)
    - `coordinate`:`[(150489, 704876), (150490, 704876), (150490, 704877), (150491, 704877), (150492, 704878), (150492, 704879), (150493, 704879), (150494, 704880), (150494, 704880), (150495, 704881)]`
    - `P`:`[6350917309492460053, 547258140500649728, 4326521518360843949, 2480463040350311882, 15166004298865807551]`
- **Sample Output**
    - `[611562904770721004, 3334895304351308538, 3894372616571971170, 6702352908935944932, 9629241829571301531]` 
---

## 6. `transfer.py.evaluate(coordinatea, coordinateb, P)`
- **Input**  
  - `coordinatea`: First set of converted Global Grid cell of level 19 coordinates.  
  - `coordinateb`: Second set of converted Global Grid cell of level 19 coordinates.  
  - `P`: A degree-100 polynomial used for hashing.
- **Output**  
  - The estimated Jaccard similarity between `coordinatea` and `coordinateb`.
- **Sample Input** (in this sample case, the degree of `P` is 5)
    - `coordinatea`:`[(150489, 704876), (150490, 704876), (150490, 704877), (150491, 704877), (150492, 704878), (150492, 704879), (150493, 704879), (150494, 704880), (150494, 704880), (150495, 704881)]`
    - `coordinateb`:`[(150486, 704873), (150487, 704873), (150487, 704874), (150488, 704874), (150488, 704875), (150489, 704876), (150490, 704876), (150490, 704877), (150491, 704877), (150492, 704878)]`
    - `P`:`[6350917309492460053, 547258140500649728, 4326521518360843949, 2480463040350311882, 15166004298865807551]`
- **Sample Output**
    - `0.4` 

---

## 7. `transfer.py.evaluateraw(coordinate1, coordinate2)`
- **Input**  
  - `coordinate1`: Original latitude/longitude points of the first route.  
  - `coordinate2`: Original latitude/longitude points of the second route.
- **Output**  
  - The estimated Jaccard similarity between the two raw routes.
- **Sample Input** 
    - `coordinate1`:`[(25.0, 121.0), (25.0001, 121.0001), (25.0002, 121.0002), (25.0003, 121.0003), (25.0004, 121.0004), (25.0005, 121.0005), (25.0006, 121.0006), (25.0007, 121.0007), (25.0008, 121.0008), (25.0009, 121.0009)]`
    - `coordinate2`:`[(24.9995, 120.9995), (24.9996, 120.9996), (24.9997, 120.9997), (24.9998, 120.9998), (24.9999, 120.9999), (25.0, 121.0), (25.0001, 121.0001), (25.0002, 121.0002), (25.0003, 121.0003), (25.0004, 121.0004)]`
- **Sample Output**
    - `0.4` 
---

## 8. `transfer.py.evaluatepath(path1, path2, path)`
- **Input**  
  - `path1`: Filename of the first `.gpx` file.  
  - `path2`: Filename of the second `.gpx` file.  
  - `path`: Output filename for the visualization image.
- **Function**  
  - Computes the similarity between the two `.gpx` routes and saves both the routes and the similarity score in the output image.

---

## 9. `transfer.py.sortpath(coors, index, K)`
- **Input**  
  - `coors`: A 2D array containing `N` routes, where each route is an array of latitude and longitude coordinates:  
    ```
    [
      [(lat₁₁, lon₁₁), ..., (lat₁ₘ_₁, lon₁ₘ_₁)],
      ...,
      [(latₙ₁, lonₙ₁), ..., (latₙₘ_ₙ), lonₙₘ_ₙ)]
    ]
    ```
  - `index`: The index of the reference route to compare with others.  
  - `K`: The number of most similar routes to output.
- **Function**  
  - Finds the top `K` most similar routes to the route at `index` and generates `K` image files showing the reference route and each of the top `K` similar routes with similarity scores.

---

## 10. `transfer.py.paintpath(coors, index, K)`
- **Input**  
  - `coors`: A 2D array containing `N` routes (same format as ```transfer.py.sortpath```).  
  - `index`: The index of the target route to compare.  
  - `K`: Number of most similar routes to visualize.
- **Function**  
  - Generates an HTML file that displays the top `K` most similar routes to the target route, along with their visual representations.
