# Evidence media

Name uploads for their claim, such as `AC-2-saved-state.png`. Keep a flow around ten seconds and GIFs below GitHub's 10 MB inline ceiling. Convert MP4 with a generated palette:

```sh
ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif
```

Embed each image or GIF as `[![AC-2 saved state](<url>)](<url>)`; the image opens at full size. Require HTTP 200, an image content type, and a PNG, JPEG, or GIF source. MP4s use ordinary links. Inspect the rendered image or representative recording frames before publication.
