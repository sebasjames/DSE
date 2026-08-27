import sys
import re

with open('platform.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS
css_code = """
        /* EASTER EGG CSS */
        .cursor-ripple {
            position: fixed;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 0, 0, 0.8);
            border-radius: 50%;
            pointer-events: none;
            z-index: 999998;
            transform: translate(-50%, -50%) scale(1);
            animation: ripple-expand 1.5s cubic-bezier(0.1, 0.8, 0.3, 1) forwards;
        }

        @keyframes ripple-expand {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; border-width: 4px; }
            100% { transform: translate(-50%, -50%) scale(8); opacity: 0; border-width: 1px; }
        }

        .fade-zoom-out {
            transition: transform 2s cubic-bezier(0.4, 0, 0.2, 1), opacity 2s ease;
            transform: scale(2.5) translateZ(0);
            opacity: 0;
            pointer-events: none;
        }

        #easter-egg-scene {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #111;
            z-index: 9999999;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 1s ease 1s;
            overflow: hidden;
            flex-direction: column;
            color: white;
            font-family: 'Inter', sans-serif;
        }

        #easter-egg-scene.egg-active {
            opacity: 1;
            pointer-events: all;
        }

        .egg-canvas {
            width: 80%;
            height: 80%;
            background: #222;
            border-radius: 20px;
            position: relative;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
            overflow: hidden;
        }

        .egg-fake-cursor {
            position: absolute;
            width: 40px;
            height: 40px;
            z-index: 100;
            top: 150%; /* Offscreen initially */
            left: 150%;
            transition: top 1s cubic-bezier(0.2, 0.8, 0.2, 1), left 1s cubic-bezier(0.2, 0.8, 0.2, 1);
            filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.5));
        }

        .egg-fake-image {
            position: absolute;
            width: 200px;
            height: 150px;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            top: -200px;
            left: 10%;
            transition: top 1s cubic-bezier(0.2, 0.8, 0.2, 1), left 1s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.3s;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 1.2rem;
            color: white;
        }
        .egg-fake-image:nth-child(2) { background: linear-gradient(135deg, #4776E6, #8E54E9); left: 80%; }
        .egg-fake-image:nth-child(3) { background: linear-gradient(135deg, #11998e, #38ef7d); left: 40%; top: 120%; }
"""

html_code = """
    <!-- EASTER EGG DOM -->
    <div id="easter-egg-scene">
        <h2 style="margin-bottom: 20px; font-weight: 300; letter-spacing: 2px;">DSE Studio Mode</h2>
        <div class="egg-canvas" id="egg-canvas">
            <div class="egg-fake-image" id="egg-img-1">Marketing Asset</div>
            <div class="egg-fake-image" id="egg-img-2">AI Output</div>
            <div class="egg-fake-image" id="egg-img-3">Data Chart</div>
            
            <svg class="egg-fake-cursor" id="egg-fake-cursor" viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg">
                <path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-41.4c-10.8-6.1-23.8-7.1-35.3-2.5s-19.5 13.8-22.1 26l-13.5 63c-3.6 16.7 1.4 34.1 13.6 46.3l128.4 128.4c12.1 12.1 28.5 18.9 45.6 18.9H320c53 0 96-43 96-96V192c0-17.7-14.3-32-32-32s-32 14.3-32 32v128h-32V64c0-17.7-14.3-32-32-32s-32 14.3-32 32v160h-32V32z" fill="#fff" stroke="#000" stroke-width="24" stroke-linejoin="round"/>
            </svg>
            <svg class="egg-fake-cursor" id="egg-fake-cursor-closed" style="display:none;" viewBox="0 0 384 512" xmlns="http://www.w3.org/2000/svg">
                <path d="M112 112c0-26.5 21.5-48 48-48s48 21.5 48 48v80c0 8.8 7.2 16 16 16s16-7.2 16-16V64c0-26.5 21.5-48 48-48s48 21.5 48 48v128c0 8.8 7.2 16 16 16s16-7.2 16-16V96c0-26.5 21.5-48 48-48s48 21.5 48 48v128c0 8.8 7.2 16 16 16s16-7.2 16-16v-16c0-26.5 21.5-48 48-48s48 21.5 48 48v224c0 70.7-57.3 128-128 128H221.3c-28.5 0-56.1-9.6-78.3-27.2L22.2 388.4C8.1 377.3 0 360.2 0 342c0-29.2 28.3-50.4 56.6-42.6L112 314.1V112z" fill="#fff" stroke="#000" stroke-width="24" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
"""

js_code = """
        // EASTER EGG LOGIC
        let rippleInterval;
        let easterEggTimeout;
        let isHolding = false;
        let mouseX = 0;
        let mouseY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        document.addEventListener('mousedown', (e) => {
            if (e.target.closest('#easter-egg-scene')) return; // Don't trigger if already inside

            isHolding = true;

            // Start Ripples
            rippleInterval = setInterval(() => {
                const ripple = document.createElement('div');
                ripple.className = 'cursor-ripple';
                ripple.style.left = mouseX + 'px';
                ripple.style.top = mouseY + 'px';
                document.body.appendChild(ripple);
                setTimeout(() => ripple.remove(), 1500);
            }, 300); // Emits a ripple every 300ms

            // Start 5 second timer
            easterEggTimeout = setTimeout(() => {
                if (isHolding) {
                    triggerEasterEgg();
                }
            }, 5000);
        });

        const stopHolding = () => {
            isHolding = false;
            clearInterval(rippleInterval);
            clearTimeout(easterEggTimeout);
        };

        document.addEventListener('mouseup', stopHolding);
        document.addEventListener('mouseleave', stopHolding);

        async function triggerEasterEgg() {
            stopHolding();
            
            // Fade and zoom the entire body content
            const children = document.body.children;
            for(let i=0; i<children.length; i++) {
                const tag = children[i].tagName.toLowerCase();
                const id = children[i].id;
                if(tag !== 'script' && tag !== 'style' && id !== 'custom-cursor' && id !== 'easter-egg-scene') {
                    children[i].classList.add('fade-zoom-out');
                }
            }

            // Hide the actual custom cursor
            document.getElementById('custom-cursor').style.display = 'none';

            // Show the easter egg scene
            const scene = document.getElementById('easter-egg-scene');
            scene.classList.add('egg-active');

            // Start the sequence after it fades in
            setTimeout(playCanvasSequence, 2000);
        }

        async function playCanvasSequence() {
            const fakeCursor = document.getElementById('egg-fake-cursor');
            const fakeCursorClosed = document.getElementById('egg-fake-cursor-closed');
            const img1 = document.getElementById('egg-img-1');
            const img2 = document.getElementById('egg-img-2');
            const img3 = document.getElementById('egg-img-3');

            const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));
            
            const moveCursor = (x, y) => {
                fakeCursor.style.left = x;
                fakeCursor.style.top = y;
                fakeCursorClosed.style.left = x;
                fakeCursorClosed.style.top = y;
            };
            
            const grab = () => {
                fakeCursor.style.display = 'none';
                fakeCursorClosed.style.display = 'block';
            };
            
            const release = () => {
                fakeCursor.style.display = 'block';
                fakeCursorClosed.style.display = 'none';
            };

            // Sequence
            moveCursor('50%', '110%'); // Start cursor bottom center
            await wait(1000);

            // Drag img1
            moveCursor('15%', '-5%'); // Go to img1
            await wait(1200);
            grab();
            await wait(200);
            img1.style.top = '20%';
            img1.style.left = '30%';
            moveCursor('35%', '25%'); // Drag it
            await wait(1200);
            release();
            await wait(500);

            // Drag img2
            moveCursor('85%', '-5%'); // Go to img2
            await wait(1200);
            grab();
            await wait(200);
            img2.style.top = '50%';
            img2.style.left = '60%';
            moveCursor('65%', '55%'); // Drag it
            await wait(1200);
            release();
            await wait(500);

            // Drag img3
            moveCursor('45%', '110%'); // Go to img3
            await wait(1200);
            grab();
            await wait(200);
            img3.style.top = '60%';
            img3.style.left = '20%';
            moveCursor('25%', '65%'); // Drag it
            await wait(1200);
            release();
            await wait(1000);
            
            // Cursor leaves
            moveCursor('150%', '150%');
        }
"""

if "EASTER EGG DOM" not in content:
    content = content.replace('</style>', css_code + '\n    </style>')
    content = content.replace('<!-- CUSTOM CURSOR DOM -->', html_code + '\n    <!-- CUSTOM CURSOR DOM -->')
    content = content.replace('// CUSTOM CURSOR LOGIC', js_code + '\n        // CUSTOM CURSOR LOGIC')
    with open('platform.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Easter Egg")
else:
    print("Already injected")
