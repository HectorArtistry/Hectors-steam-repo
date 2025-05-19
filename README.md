# Raw Data Description

This project uses several structured datasets containing detailed information about Steam games and their associated metadata. 
This data was pulled in October 2024 and took the author 150 hours to pull.
## API(s) used
- "api.steampowered.com/ISteamApps/GetAppList/v2" was used to fetch the steam catalog data.
- "store.steampowered.com/api/appdetails?appids=<appid>" was used for basic game details
  - *Example:* "tore.steampowered.com/api/appdetails?appids=240"
- "store.steampowered.com/appreviews/<appid>" was used to pull game reviews
  - *Example:* "store.steampowered.com/appreviews/240?json=1&language=english&filter=all"
- "steamspy.com/api.php?request=appdetails&appid=<APPID>" was used to pull game insights like player count. 
  - *Note:* Steamspy is a third party site.
  - *Example:* "steamspy.com/api.php?request=appdetails&appid=240"
- "store.steampowered.com/app/<APPID>" was used to web scrape game tags.
  - *Example:* "store.steampowered.com/app/240"

## Below is a description of each raw dataset:

### `games.csv`
- Main table containing core details about the games.
- Includes title, release date, and additional metadata.

### `genres.csv`
- Lists the genres assigned to each game.

### `tags.csv`
- Contains tags associated with each game (e.g., "Indie", "Action", etc.).

### `reviews.csv`
- Review data for the games.
- Includes Steam ratings and review counts.

### `steamspy_insights.csv`
- Insights gathered from SteamSpy.
- Provides data such as estimated sales, playtime, and more.

### `descriptions.csv`
- Contains full and summary text descriptions of each game.

### `promotional.csv`
- Links and metadata for promotional materials.
- Includes trailers, screenshots, and other marketing assets.

### `categories.csv`
- Information about Steam categories each game belongs to.
- Examples: "Single-player", "Full controller support", etc.