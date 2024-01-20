

// load virtual tour json data
async function load_tour_json_data(src, callback) {
    try {
            // Fetch the JSON File
            const options = {
                method: 'GET',
                mode: 'cors'
            }

            const response = await fetch(src, options);

            // check if fetch was successful
            if(!response.ok) {
                throw new Error('Failed to load Virtual Tour data');
            }

            // parse the json data
            const jsonData = await response.text();
            //console.log(jsonData);

            var tour_data = JSON.parse(jsonData);
            //console.log(tour_data);
            callback(tour_data);
        
    } catch (Error) {
        console.log(Error);
    }
}




export function show_tour(tour_data_url) {
    console.log('Hello from tour viewer.');
    console.log(tour_data_url)
    load_tour_json_data(tour_data_url, tour_data => {
    // load apporpiate tour
    pannellum.viewer("panorama", tour_data);
});
}

window.show_tour = show_tour;

export function show_new_tour(tour_data_url) {
    console.log('Opening new tour.');
    load_tour_json_data(tour_data_url, tour_data => {
        // load apporpiate tour
        document.getElementById('panorama').innerHTML = '';
        pannellum.viewer("panorama", tour_data);
    });
}

window.show_new_tour = show_new_tour;


// load_tour_json_data('https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/Virtual_Tours/testing/example_tour.json').then(jsonData => {
//     console.log(jsonData);
//     console.log(pannellum);
//     pannellum.viewer(jsonData);
// }); 
  


// function start_virtual_tour_viewer(viewer_json_data) {
//     console.log('Recieved Json Data '+ viewer_json_data)
//     pannellum.viewer(viewer_json_data);
// }

/*
'panorama', {
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
            "panorama": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/Virtual_Tours/Ridgewood_example/DJI_0010.JPG",
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
            "panorama": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/Virtual_Tours/Ridgewood_example/DJI_0005.JPG",
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
            "panorama": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/Virtual_Tours/Ridgewood_example/DJI_0007.JPG",
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
            "panorama": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/Virtual_Tours/Ridgewood_example/DJI_0009.JPG",
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
}
*/