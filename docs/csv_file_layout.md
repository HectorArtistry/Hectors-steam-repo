## CSV Table Structure

| Table Name         | Columns |
|--------------------|---------|
| `categories`       | `appid`, `categories` |
| `descriptions`     | `appid`, `summary`, `extensive`, `about` |
| `games`            | `appid`, `name`, `release date`, `is_free`, `price_overview`, `languages`, `type` |
| `genres`           | `appid`, `genre` |
| `promotional`      | `appid`, `header_image`, `background_image`, `screenshots`, `movies` |
| `reviews`          | `appid`, `review_score`, `review_score description`, `positive`, `negative`, `total`, `metacritic_score`, `reviews`, `recommendations`, `steamspy_user_score`, `steamspy_score_rank`, `steamspy_positive`, `steamspy_negative` |
| `steamspy_insights`| `appid`, `developer`, `publisher`, `owners_range`, `playtime_average_forever`, `playtime_average_2weeks`, `playtime_median_forever`, `playtime_median_forever`, `price`, `initial_price`, `discount`, `languages`, `genres` |
| `tags`             | `appid`, `tag` |

# Note #
- The "game" table has a sets in several of its columns.
-  