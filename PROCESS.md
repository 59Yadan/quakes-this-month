# Process

## Tools

I used DeepSeek as a coding assistant throughout this assignment. It
wrote the draft of `plot.py` — the loading function, the scatter plot,
the depth colourbar, and the date ticks. It also helped me diagnose why
`fetch.py` could not reach the USGS feed and suggested the EMSC Seismic
Portal as an alternative.

## Kept

**The switch from USGS to EMSC as the data source.**

The first version of `fetch.py` used the USGS 2.5-month feed, which is
one of the sources the assignment lists. But from my network the request
timed out — `requests.exceptions.ConnectTimeout` after the full
60-second timeout. DeepSeek suggested EMSC instead. The Seismic Portal
is a European federation and its server was reachable from my network.

I kept this change because it worked and because the phenomenon is the
same: earthquakes, measured continuously, published openly. The data
structure is close enough to USGS that `plot.py` only needed small
changes, but the fields are not identical — EMSC sends `time` as an
ISO 8601 string and `depth` as a positive number in `properties.depth`,
while USGS puts the depth in `geometry.coordinates[2]`.

**The two functions in `plot.py` — `load_quakes` and `main`.**

DeepSeek split the script into a loader that reads the GeoJSON and
returns a list of `(datetime, magnitude, depth)` tuples, and a `main`
that does everything else. I left that split as it was, and it turned
out to be useful: when I later changed the point size, the date ticks,
and the title, I only had to touch `main` — `load_quakes` stayed as it
was.

## Rejected

- **`vmin=0, vmax=150` on the colour map.** The idea was to stop the
  shallow quakes all appearing the same pale colour. I tried it and
  decided against it: capping the range would draw every deep quake in
  the same shade, and the assignment asks the picture to say what the
  data actually is. I left the default range and let the colour do what
  it does — most quakes shallow, a few very deep.

- **Switching the colour map from `viridis_r` to `Blues` or `magma_r`.**
  I tried both. They looked worse to me — the contrast between shallow
  and deep was less clear — so I kept `viridis_r`.

## What I changed myself

- **Point size.** I changed it from 12 to 9. At 4352 points, size 12
  overlapped into a solid block and the individual quakes were no
  longer visible.

- **Date ticks.** The default auto-ticks were showing only every other
  day, so I asked for one tick per day. DeepSeek supplied the two
  `mdates` lines that do it, and I added them.

- **The title.** I noticed the data ends on 19 September, not the whole
  month — the URL asks for the full month, but the file was fetched on
  the 19th, so the last eleven days had not happened. I changed the
  figure title to say 1–19 September.

- **`plt.show()`.** The code DeepSeek generated did not call
  `plt.show()`, so running `uv run plot.py` finished without showing
  the picture. I looked at the week-3 example, which does call it, and
  added the line — now the figure pops up as soon as the script runs.