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
        
    # Extract original width and height
    w_m = re.search(r'width="(\d+)"', svg_data)
    h_m = re.search(r'height="(\d+)"', svg_data)
    orig_w = int(w_m.group(1)) if w_m else 663
    orig_h = int(h_m.group(1)) if h_m else 104
    
    # We will "extend the picture" to make it look full and not half-baked.
    new_w = orig_w + 40
    new_h = orig_h + 80
    
    active_blocks = []
    rects = re.findall(r'<rect([^>]+)>', svg_data)
    for rect in rects:
        x_m = re.search(r'x="(\d+)"', rect)
        y_m = re.search(r'y="(\d+)"', rect)
        fill_m = re.search(r'fill:#([a-fA-F0-9]+)', rect)
        
        if x_m and y_m and fill_m:
            x, y = int(x_m.group(1)), int(y_m.group(1))
            fill_hex = fill_m.group(1).upper()
            if fill_hex != 'EEEEEE':
                active_blocks.append((x, y))
                
    if not active_blocks:
        active_blocks = [(10, 10), (20, 20), (30, 30), (40, 40)]
        
    active_blocks.sort(key=lambda b: (b[0], b[1]))
    
    keyframes = ""
    total_points = len(active_blocks)
    for i, (x, y) in enumerate(active_blocks):
        percent = (i / max(1, total_points - 1)) * 100
        # Offset character slightly above the block
        keyframes += f"            {percent:.1f}% {{ transform: translate({x-6}px, {y-18}px); }}\n"
        
    style = f"""
    <style>
        @keyframes walkPath {{
{keyframes}
        }}
        .miner-char {{
            animation: walkPath {max(5, total_points*0.4)}s steps(1) infinite;
            font-size: 18px;
            text-shadow: 0 0 5px rgba(0,255,0,0.5);
        }}
        .title-text {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            fill: #7ee787;
        }}
        .bg-rect {{
            fill: #0d1117;
            rx: 10px;
        }}
        .grid-group {{
            transform: translate(20px, 40px);
        }}
    </style>
    """
    
    miner_svg = f'''
        <text class="miner-char" x="0" y="10">🦊⛏️</text>
    '''
    
    # Clean up original SVG wrapper
    inner_content = re.sub(r'<svg[^>]*>', '', svg_data)
    inner_content = inner_content.replace('</svg>', '')
    
    # Replace old colors with TokyoNight dark colors
    inner_content = inner_content.replace('fill:#EEEEEE', 'fill:#161B22')
    inner_content = inner_content.replace('fill:#767676', 'fill:#8B949E')
    inner_content = inner_content.replace('fill:#c6e48b', 'fill:#0e4429')
    inner_content = inner_content.replace('fill:#7bc96f', 'fill:#006d32')
    inner_content = inner_content.replace('fill:#239a3b', 'fill:#26a641')
    inner_content = inner_content.replace('fill:#196127', 'fill:#39d353')
    
    # Build the EXTENDED new SVG
    new_svg = f'''<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{new_w}" height="{new_h}" viewBox="0 0 {new_w} {new_h}">
    {style}
    <rect class="bg-rect" width="{new_w}" height="{new_h}" />
    
    <!-- Header Title -->
    <text class="title-text" x="20" y="25">🦊 Commits Mined in Real-Time</text>
    
    <!-- Minecraft-like dirt floor below the graph -->
    <rect fill="#3b2d20" x="0" y="{new_h - 15}" width="{new_w}" height="15" />
    <rect fill="#2a823b" x="0" y="{new_h - 20}" width="{new_w}" height="5" />
    
    <!-- The actual contribution graph shifted down -->
    <g class="grid-group">
        {inner_content}
        {miner_svg}
    </g>
</svg>'''

    with open('mining_graph.svg', 'w', encoding='utf-8') as f:
        f.write(new_svg)
        
    print("Successfully generated extended valid CSS-animated mining_graph.svg!")

if __name__ == "__main__":
    build_miner_svg()
