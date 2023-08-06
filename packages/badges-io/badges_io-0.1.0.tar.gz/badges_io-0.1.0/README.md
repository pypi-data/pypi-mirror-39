# badges_io

Uploads total badge data to https://badges-io.now.sh service.

## Usage
Just issue

    python3 -m badges_io coverage 97%

Here the "coverage" is a subject appearing to the left in the badge, while
"97%" here is the status of the badge, appearing to the right.

The color of the badge will be auto computed from the status. A third argument
will override the color, e.g. "green".

to upload coverage to the badges service. `badges_io` will try to autodetect the
repo slug (e.g. "user/repo") by first looking at the origin remote of the
current git repo, and also using environment variables if run on Travis CI.

## Author
Samuel Carlsson
