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
        
    # Find all colored rectangles representing commits
    rects = re.findall(r'<rect [^>]*x="(\d+)"[^>]*y="(\d+)"[^>]*fill="([^"]+)"[^>]*>', svg_data)
    
    active_blocks = []
    for x, y, fill in rects:
        # #ebedf0 is the default empty grey block color in ghchart
        if fill != '#ebedf0':
            active_blocks.append((int(x), int(y)))
            
    # Fallback path if you have 0 commits
    if not active_blocks:
        active_blocks = [(10, 10), (20, 20), (30, 30), (40, 40)]
        
    # Sort them to make the character move from left to right (chronological)
    active_blocks.sort(key=lambda b: (b[0], b[1]))
    
    path_points = [f"{x},{y}" for x, y in active_blocks]
    path_d = "M " + " L ".join(path_points)
    
    # Inject a style for the miner to bounce/mine while moving
    style = """
    <style>
        @keyframes mine {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-3px) rotate(-15deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        .miner-char {
            animation: mine 0.4s infinite;
        }
    </style>
    """
    
    # 🦊⛏️ A cute fox miner
    miner_svg = f'''
    <g id="miner" transform="translate(-8, -15)">
        <text class="miner-char" x="0" y="10" font-size="16">🦊⛏️</text>
        <animateMotion path="{path_d}" dur="{max(5, len(active_blocks)*0.15)}s" repeatCount="indefinite" />
    </g>
    '''
    
    svg_data = svg_data.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')
    svg_data = svg_data.replace('</svg>', style + miner_svg + '\n</svg>')
    
    # Make background TokyoNight dark
    svg_data = re.sub(r'<svg([^>]*)>', r'<svg\1 style="background-color:#0D1117; border-radius: 8px; padding: 10px;">', svg_data, count=1)
    
    # Replace default light theme colors to match TokyoNight Dark Mode
    svg_data = svg_data.replace('#ebedf0', '#161B22')
    svg_data = svg_data.replace('#767676', '#8B949E')
    
    with open('mining_graph.svg', 'w', encoding='utf-8') as f:
        f.write(svg_data)
        
    print("Successfully generated mining_graph.svg!")

if __name__ == "__main__":
    build_miner_svg()
