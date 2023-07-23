import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import WebGL from 'three/addons/capabilities/WebGL.js';

// Check if WebGL is supported by browser.
if( WebGL.isWebGLAvailable()) {
    console.log("WebGL Supported")
} else {
    const warning = WebGL.getWebGLErrorMessage();
    document.getElementById('Model-Viewer').appendChild(warning);
}

const canvas = document.querySelector('#Model-Viewer');
const renderer = new THREE.WebGLRenderer({antialias: true, canvas});

// camera setup
const fov = 75;
const aspect = 2; // the canvas default
const near = 0.1;
const far = 1000;
const camera = new THREE.PerspectiveCamera(fov, window.innerWidth / window.innerHeight, near, far);

renderer.setSize(window.innerWidth/2, window.innerHeight/2, true)

camera.position.z = 14;

// Scene setup
const scene = new THREE.Scene();

// Geometry setup
const boxWidth = 3;
const boxHeight = 3;
const boxDepth = 3;
const geometry = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);

// Create Mesh Material
const material = new THREE.MeshBasicMaterial({color: 0x44aa88});

const cube = new THREE.Mesh(geometry, material);

// Add Geometry to scene
scene.add(cube);

function Rotate(geometry_) {
    requestAnimationFrame( Rotate );

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera)
}

// Draw Lines
function drawLines() {
    const line_material = new THREE.LineBasicMaterial( { color: 0x67FF00 } );

    const points = [];
    points.push(new THREE.Vector3( -10, 0, 0));
    points.push(new THREE.Vector3( 0, 10, 0));
    points.push(new THREE.Vector3( 10, 0, 0));
    points.push(new THREE.Vector3( 0, -10, 0));
    
    const geometry = new THREE.BufferGeometry().setFromPoints( points );
    
    const line = new THREE.Line( geometry, line_material);
    
    scene.add(line);
    
    // Render Scene
    renderer.render(scene, camera)
}

drawLines();
Rotate(cube);
