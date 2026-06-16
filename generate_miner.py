import urllib.request
import re

def build_miner_svg():
    url = "https://ghchart.rshah.org/40c463/nadeemsahu"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching SVG: {e}")
        return
        
    # Find all rectangles
    active_blocks = []
    rects = re.findall(r'<rect([^>]+)>', svg_data)
    for rect in rects:
        x_m = re.search(r'x="(\d+)"', rect)
        y_m = re.search(r'y="(\d+)"', rect)
        fill_m = re.search(r'fill:#([a-fA-F0-9]+)', rect)
        
        if x_m and y_m and fill_m:
            x, y = int(x_m.group(1)), int(y_m.group(1))
            fill_hex = fill_m.group(1).upper()
            # EEEEEE is the empty gray block
            if fill_hex != 'EEEEEE':
                active_blocks.append((x, y))
                
    if not active_blocks:
        active_blocks = [(10, 10), (20, 20), (30, 30), (40, 40)]
        
    # Sort them to make the character move chronologically (left to right)
    active_blocks.sort(key=lambda b: (b[0], b[1]))
    
    # Generate CSS keyframes for movement
    keyframes = ""
    total_points = len(active_blocks)
    for i, (x, y) in enumerate(active_blocks):
        percent = (i / max(1, total_points - 1)) * 100
        keyframes += f"            {percent:.1f}% {{ transform: translate({x-8}px, {y-15}px); }}\n"
        
    style = f"""
    <style>
        @keyframes walkPath {{
{keyframes}
        }}
        .miner-char {{
            animation: walkPath {max(5, total_points*0.3)}s steps(1) infinite;
            font-size: 16px;
        }}
    </style>
    """
    
    # 🦊⛏️ A cute fox miner
    miner_svg = f'''
    <g id="miner">
        <text class="miner-char" x="0" y="10">🦊⛏️</text>
    </g>
    '''
    
    if 'xmlns="http://www.w3.org/2000/svg"' not in svg_data:
        svg_data = svg_data.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        
    svg_data = svg_data.replace('</svg>', style + miner_svg + '\n</svg>')
    
    svg_data = re.sub(r'<svg([^>]*)>', r'<svg\1 style="background-color:#0D1117; border-radius: 8px; padding: 10px;">', svg_data, count=1)
    
    svg_data = svg_data.replace('fill:#EEEEEE', 'fill:#161B22')
    svg_data = svg_data.replace('fill:#767676', 'fill:#8B949E')
    
    with open('mining_graph.svg', 'w', encoding='utf-8') as f:
        f.write(svg_data)
        
    print("Successfully generated valid CSS-animated mining_graph.svg!")

if __name__ == "__main__":
    build_miner_svg()
