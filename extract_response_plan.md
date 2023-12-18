## Example Response

`{
	"botanist": {
		"email": "carl.linnaeus@lnhm.co.uk",
		"name": "Carl Linnaeus",
		"phone": "(146)994-1635x35992"
	},
	"images": {
		"license": 451,
		"license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
		"license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
		"medium_url": "https://perenual.com/storage/image/upgrade_access.jpg",
		"original_url": "https://perenual.com/storage/image/upgrade_access.jpg",
		"regular_url": "https://perenual.com/storage/image/upgrade_access.jpg",
		"small_url": "https://perenual.com/storage/image/upgrade_access.jpg",
		"thumbnail": "https://perenual.com/storage/image/upgrade_access.jpg"
	},
	"last_watered": "Sun, 17 Dec 2023 14:56:18 GMT",
	"name": "Pitcher plant",
	"origin_location": [
		"22.88783",
		"84.13864",
		"Jashpurnagar",
		"IN",
		"Asia/Kolkata"
	],
	"plant_id": 5,
	"recording_taken": "2023-12-18 12:23:36",
	"scientific_name": [
		"Sarracenia catesbaei"
	],
	"soil_moisture": 26.927145724692537,
	"temperature": 23.560744633314833
}`

## Errors list:

- `{'error': 'plant not found', 'plant_id': 7}`

- `{'error': 'plant sensor fault', 'plant_id': 15}`

- `{'error': 'plant on loan to another museum', 'plant_id': 43}`