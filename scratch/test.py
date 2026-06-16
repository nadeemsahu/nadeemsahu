import urllib.request
import re
import random

def build_miner_svg():
    # Fetch user's contribution SVG
    url = "https://ghchart.rshah.org/40c463/nadeemsahu"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching SVG: {e}")
        return
        
    # Parse rects
    # <rect class="day" width="10" height="10" x="14" y="0" fill="#ebedf0" data-count="0" data-date="2023-01-01"/>
    rects = re.findall(r'<rect [^>]*x="(\d+)"[^>]*y="(\d+)"[^>]*fill="([^"]+)"[^>]*>', svg_data)
    
    active_blocks = []
    for x, y, fill in rects:
        # standard github empty block is #ebedf0
        if fill != '#ebedf0':
            active_blocks.append((int(x), int(y)))
            
    if not active_blocks:
        active_blocks = [(10, 10), (20, 20), (50, 50)] # fallback
        
    # shuffle or sort blocks for the path
    # Let's sort them by x then y so it moves left to right
    active_blocks.sort(key=lambda b: (b[0], b[1]))
    
    # take a subset to avoid huge paths, e.g., max 50 blocks
    if len(active_blocks) > 50:
        active_blocks = random.sample(active_blocks, 50)
        active_blocks.sort(key=lambda b: (b[0], b[1]))
        
    path_points = [f"{x},{y}" for x, y in active_blocks]
    path_d = "M " + " L ".join(path_points)
    
    # Miner character (a simple Minecraft-like pickaxe or small character)
    miner_svg = f'''
    <g id="miner" transform="translate(-5, -15)">
        <!-- A small cute pickaxe/miner -->
        <text x="0" y="10" font-size="12" font-family="Arial">⛏️</text>
        <animateMotion path="{path_d}" dur="{len(active_blocks)*0.5}s" repeatCount="indefinite" />
    </g>
    '''
    
    # Inject before the closing </svg>
    svg_data = svg_data.replace('</svg>', miner_svg + '\n</svg>')
    
    with open('output.svg', 'w', encoding='utf-8') as f:
        f.write(svg_data)
        
    print("Done generating output.svg!")

if __name__ == "__main__":
    build_miner_svg()
