pannellum.viewer('panorama', {
    "default": {
        "firstScene": "school_intrance",
        "author": "Zion Johnson",
        "sceneFadeDuration": 1000,
        "autoLoad": true
    },

    "scenes": {
        "field": {
            "title": "playground field",
            "hfov": 95,
            "pitch": 0,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "./static/360s/DJI_0010.JPG",
            "hotSpots": [
                {
                    "pitch": -14,
                    "yaw": 42,
                    "type": "scene",
                    "text": "Ridge Wood Elementry Intrance",
                    "sceneId": "school_intrance"
                },
                {
                    "pitch": -19,
                    "yaw": 5,
                    "type": "scene",
                    "text": "Playground",
                    "sceneId": "playground"
                },
                {
                    "pitch": -13,
                    "yaw": 7.5,
                    "type": "scene",
                    "text": "Basket Ball Court",
                    "sceneId": "basket_ball_court"
                }
            ]
        },
        "school_intrance": {
            "title": "School Intrance",
            "hfov": 95,
            "pitch": 0,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "./static/360s/DJI_0005.JPG",
            "hotSpots": [
                {
                    "pitch": -2,
                    "yaw": 7,
                    "type": "info",
                    "text": "Ridge Wood Elementry"
                },
                {
                    "pitch": -18,
                    "yaw": 180,
                    "type": "info",
                    "text": "Parking Lot"
                },
                {
                    "pitch": -2,
                    "yaw": -30,
                    "type": "scene",
                    "text": "Playground Field",
                    "sceneId": "field"
                }
            ]
        },
        "playground": {
            "title": "Playground",
            "hfov": 95,
            "pitch": 0,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "static/360s/DJI_0007.JPG",
            "hotSpots": [
                {
                    "pitch": -10,
                    "yaw": 5,
                    "type": "scene",
                    "text": "Basket Ball Court",
                    "sceneId": "basket_ball_court"
                },
                {
                    "pitch": 2,
                    "yaw": 172,
                    "type": "scene",
                    "text": "Play Ground Field",
                    "sceneId": "field"
                },
                {
                    "pitch": -6,
                    "yaw": 82,
                    "type": "scene",
                    "text": "School Entrance",
                    "sceneId": "school_intrance"
                }

            ]
        },
        "basket_ball_court": {
            "title": "Basket Ball Court",
            "hfov": 95,
            "pitch": 0,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "static/360s/DJI_0009.JPG",
            "hotSpots": [
                {
                    "pitch": 3,
                    "yaw": 0,
                    "type": "scene",
                    "text": "playground field",
                    "sceneId": "field"
                },
                {
                    "pitch": -7,
                    "yaw": 12,
                    "type": "scene",
                    "text": "playground",
                    "sceneId": "playground"
                }
            ]
        }

    }
});