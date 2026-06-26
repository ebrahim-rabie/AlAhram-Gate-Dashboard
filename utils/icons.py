"""
AlAhram Gate Dashboard — Custom SVG Icons
Contains minimalist vector icons for KPI cards.
"""

def get_svg_icon(name: str) -> str:
    """Return an SVG string for the given icon name."""
    
    # Base styling applied to all SVGs: inherit color (which will be set via CSS to Red/Gold)
    base_svg = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'

    icons = {
        "car": f'<svg {base_svg}><path d="M14 16H9m10 0h3v-3.15a1 1 0 00-.84-.99L16 11l-2.7-3.6a2 2 0 00-1.6-.8H9.3a2 2 0 00-1.6.8L5 11l-5.16.86a1 1 0 00-.84.99V16h3m10 0a2 2 0 104 0m-4 0a2 2 0 11-4 0m-10 0a2 2 0 104 0m-4 0a2 2 0 11-4 0"></path></svg>',
        
        "electric": f'<svg {base_svg}><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path></svg>',
        
        "new": f'<svg {base_svg}><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>',
        
        "used": f'<svg {base_svg}><path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>',
        
        "brand": f'<svg {base_svg}><path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>',
        
        "world": f'<svg {base_svg}><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"></path><path d="M2 12h20"></path></svg>',
        
        "calendar": f'<svg {base_svg}><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
        
        "trophy": f'<svg {base_svg}><path d="M8 21h8M12 17v4M7 4h10M5 4h14v5c0 3.87-3.13 7-7 7s-7-3.13-7-7V4z"></path></svg>',
        
        "location": f'<svg {base_svg}><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>',
        
        "engine": f'<svg {base_svg}><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"></path></svg>',
        
        "document": f'<svg {base_svg}><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
        
        "tool": f'<svg {base_svg}><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"></path></svg>',
        
        "fuel": f'<svg {base_svg}><path d="M3 22v-8c0-1.1.9-2 2-2h4c1.1 0 2 .9 2 2v8"></path><path d="M11 17h6c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2h-1V5c0-1.1-.9-2-2-2h-3"></path><line x1="3" y1="22" x2="11" y2="22"></line></svg>',
    }
    
    # Fallback to a generic circle/dot if icon not found
    fallback = f'<svg {base_svg}><circle cx="12" cy="12" r="10"></circle></svg>'
    
    return icons.get(name, fallback)
