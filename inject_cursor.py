import sys

with open('platform.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_code = """
        /* CUSTOM CURSOR */
        body, a, button, .nav-cta, input, textarea {
            cursor: none !important;
        }

        #custom-cursor {
            position: fixed;
            top: 0;
            left: 0;
            width: 40px;
            height: 40px;
            pointer-events: none;
            z-index: 999999;
            transform: translate(-20px, -10px); /* Adjust so the tip is at the mouse coordinate */
            transition: transform 0.05s linear;
        }

        .cursor-icon {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            transition: opacity 0.15s ease;
            filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
        }

        .cursor-icon.active {
            opacity: 1;
        }

        .cursor-click-lines {
            position: absolute;
            top: -15px;
            left: -15px;
            width: 70px;
            height: 70px;
            opacity: 0;
            pointer-events: none;
        }

        .cursor-click-lines path {
            stroke: #333;
            stroke-width: 3;
            stroke-linecap: round;
            stroke-dasharray: 20;
            stroke-dashoffset: 20;
        }

        body.is-clicking .cursor-click-lines {
            opacity: 1;
        }

        body.is-clicking .cursor-click-lines path {
            animation: click-burst 0.4s ease-out forwards;
        }

        @keyframes click-burst {
            0% { stroke-dashoffset: 20; opacity: 1; transform: scale(0.8); transform-origin: center; }
            50% { stroke-dashoffset: 0; opacity: 1; transform: scale(1.1); transform-origin: center; }
            100% { stroke-dashoffset: -20; opacity: 0; transform: scale(1.2); transform-origin: center; }
        }

        /* Prevent default dragging cursors */
        * {
            user-select: none;
        }
        input, textarea, p, h1, h2, h3, h4, h5, h6, span {
            user-select: text; /* Allow text selection */
        }
"""

html_code = """
    <!-- CUSTOM CURSOR DOM -->
    <div id="custom-cursor">
        <!-- Lines -->
        <svg class="cursor-click-lines" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M 50 15 L 50 5" fill="none" />
            <path d="M 25 25 L 15 15" fill="none" />
            <path d="M 75 25 L 85 15" fill="none" />
            <path d="M 15 50 L 5 50" fill="none" />
            <path d="M 85 50 L 95 50" fill="none" />
        </svg>

        <!-- Pointing Hand (Normal) -->
        <svg class="cursor-icon active" id="cursor-point" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <path d="M26,30 V12 c0,-3.3 2.7,-6 6,-6 c3.3,0 6,2.7 6,6 v18 c0,0 3,-1 5,0 c3,1 4,4 4,4 l4,10 c1,2.5 1,6 -1,9 c-2,3 -6,5 -10,5 H26 c-5,0 -10,-3 -12,-7 l-6,-8 c-2,-2.5 -1,-6 2,-7 c2.5,-1 5.5,0.5 7,3 l3,4 V30 Z" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/>
        </svg>

        <!-- Open Hand (2 Fingers / Hovering Draggable) -->
        <svg class="cursor-icon" id="cursor-open" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <path d="M20,30 V16 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v14 h2 V14 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v16 h2 V20 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v18 c0,4 -2,8 -5,11 H28 c-4,0 -8,-2 -11,-5 l-5,-6 c-2,-2 -2,-5 0,-7 l4,-4 c2,-2 5,-2 7,0 l1,1 V30 Z" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/>
        </svg>

        <!-- Closed Hand (Dragging) -->
        <svg class="cursor-icon" id="cursor-closed" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <path d="M18,34 l-5,-4 c-2,-2 -2,-5 0,-7 c2,-2 5,-2 7,0 l4,4 V22 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v8 c0,3 5,3 5,0 v-4 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v6 c0,3 5,3 5,0 v-2 c0,-3 2.5,-5 5,-5 c2.5,0 5,2 5,5 v18 c0,4 -2,8 -5,11 H28 c-4,0 -8,-2 -11,-5 Z" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/>
        </svg>
    </div>
"""

js_code = """
        // CUSTOM CURSOR LOGIC
        const cursor = document.getElementById('custom-cursor');
        const iconPoint = document.getElementById('cursor-point');
        const iconOpen = document.getElementById('cursor-open');
        const iconClosed = document.getElementById('cursor-closed');
        let isDraggingCursor = false;
        let isSelecting = false;

        document.addEventListener('mousemove', (e) => {
            cursor.style.transform = `translate(${e.clientX - 16}px, ${e.clientY - 8}px)`;
            
            // Check if user is selecting text
            if (window.getSelection().toString().length > 0 && e.buttons === 1) {
                isSelecting = true;
                setCursorState(iconOpen);
            } else if (isSelecting && e.buttons === 0) {
                isSelecting = false;
                if (!isDraggingCursor) setCursorState(iconPoint);
            }
        });

        document.addEventListener('mousedown', (e) => {
            // Trigger click burst
            document.body.classList.remove('is-clicking');
            void document.body.offsetWidth; // trigger reflow
            document.body.classList.add('is-clicking');
            setTimeout(() => document.body.classList.remove('is-clicking'), 400);

            // Handle Drag/Selection start
            if (e.target.tagName.toLowerCase() !== 'input' && e.target.tagName.toLowerCase() !== 'textarea') {
                isDraggingCursor = true;
                setCursorState(iconClosed);
            }
        });

        document.addEventListener('mouseup', () => {
            isDraggingCursor = false;
            if (!isSelecting) {
                setCursorState(iconPoint);
            }
        });

        function setCursorState(activeIcon) {
            iconPoint.classList.remove('active');
            iconOpen.classList.remove('active');
            iconClosed.classList.remove('active');
            activeIcon.classList.add('active');
        }
"""

if "CUSTOM CURSOR DOM" not in content:
    if "/* CUSTOM CURSOR */" not in content:
        content = content.replace('</style>', css_code + '\n    </style>')
    content = content.replace('</body>', html_code + '\n<script>\n' + js_code + '\n</script>\n</body>')
    with open('platform.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected cursor code")
else:
    print("Already injected")
