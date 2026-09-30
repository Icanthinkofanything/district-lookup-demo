# Voting district lookup (demo)

Type a street address in Vanderburgh County, Indiana (or click the map) and see its precinct, township, county, state house, state senate and congressional district.

**[▶ Live demo](https://icanthinkofanything.github.io/district-lookup-demo/)**

- Boundaries: U.S. Census Bureau TIGERweb (2020 voting districts, county subdivisions, 2026 state legislative districts, 119th congressional districts), clipped to the county.
- Address matching: the free U.S. Census geocoder (no API key).
- Point-in-polygon: Turf.js in the browser. Static files, so no server and no ongoing cost; it can be embedded in WordPress with an iframe or a custom HTML block.

`build.py` downloads and prepares the boundary layers.
