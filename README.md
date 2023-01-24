# Marker

Marker is an automation tool to mark a list of movie/shows/series as watched in Douban (豆瓣). This tool is useful if you want to migrate your movie list from another app to Douban.

## Usage

### Extract the movie list from images (Optional)

Many mobile applications do not support exporting the movie list. One easy automated solution is to read the movie name from the screenshots using OCR.
You can save all the screenshots in a folder and execute the following command.
As a result, a `list.csv` file will be produced with all the extracted media names.

```bash
mark -e <image-folder>
```

> Some manual editing may be required for the extracted movie names as OCR is not 100% accurate.
> The generated file will assign a default score the movie, default is 8.

### Mark on Douban

You can either prepare the `list.csv` with the command given above or create on your own manually.
Once this file is ready, just execute the following command to mark the list of media as watched on Douban.


```bash
mark -f list.csv
```
