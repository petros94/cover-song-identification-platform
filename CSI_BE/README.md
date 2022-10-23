### Get all songs
curl -X GET "http://localhost:5000/songs"

Response:
[
  {
    "_id": "6351c405c0303fbe8812c449",
    "title": "Summer Wine [79CR6prA-jI]",
    "upload_date": "Thu, 20 Oct 2022 21:56:21 GMT",
    "version": "1.0",
    "yt_link": "https://www.youtube.com/watch?v=79CR6prA-jI"
  },
  {
    "_id": "6351d342fcf2548e0a169853",
    "title": "Summer Wine (Single Edit) [KIvz5zYXCoI]",
    "upload_date": "Thu, 20 Oct 2022 23:01:22 GMT",
    "version": "1.0",
    "yt_link": "https://www.youtube.com/watch?v=KIvz5zYXCoI"
  }
]

### Upload song
curl -X POST http://localhost:5000/songs -H "Content-Type: application/json" -d '{"yt_link": "https://www.youtube.com/watch?v=79CR6prA-jI"}'

Response:
{
    "_id": "6351c405c0303fbe8812c449",
    "title": "Summer Wine [79CR6prA-jI]",
    "upload_date": "Thu, 20 Oct 2022 21:56:21 GMT",
    "version": "1.0",
    "yt_link": "https://www.youtube.com/watch?v=79CR6prA-jI"
}

### Predict pair
curl -X GET "http://localhost:5000/predict/pair?id_1=6351c405c0303fbe8812c449&id_2=6351c405c0303fbe8812c449"

Response:
{
  "dist": 0.0,
  "is_cover": 1
}

