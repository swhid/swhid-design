#!/usr/bin/env python3
"""
SWHID Navbar Injection Script

This script injects the unified SWHID navigation bar into built HTML files
from MkDocs sites. It's designed to be used in the bootstrap scripts
as a more robust alternative to sed expressions.
"""

import os
import sys
import re
import argparse
from pathlib import Path


def load_navbar_html(plugin_dir):
    """Load the navbar HTML template."""
    navbar_file = os.path.join(plugin_dir, 'unified-navbar.html')
    if os.path.exists(navbar_file):
        with open(navbar_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def load_navbar_css(plugin_dir):
    """Load the navbar CSS."""
    css_file = os.path.join(plugin_dir, 'unified-navbar.css')
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def inject_navbar_into_html(html_content, navbar_html):
    """Inject the navbar into HTML content."""
    if not navbar_html:
        return html_content
    
    # Look for <body class="wy-body-for-nav"> or just <body>
    body_pattern = r'(<body[^>]*>)'
    if re.search(body_pattern, html_content):
        html_content = re.sub(body_pattern, r'\1\n' + navbar_html, html_content, count=1)
    else:
        # Fallback: inject after <body> tag
        html_content = html_content.replace('<body>', '<body>\n' + navbar_html, 1)
    
    return html_content


def inject_css_into_html(html_content, css_content):
    """Inject CSS into HTML content."""
    if not css_content:
        return html_content
    
    # Look for </head> tag
    if '</head>' in html_content:
        css_tag = f'<style type="text/css">\n{css_content}\n</style>\n'
        html_content = html_content.replace('</head>', css_tag + '</head>')
    else:
        # Fallback: inject after <head> tag
        css_tag = f'<style type="text/css">\n{css_content}\n</style>\n'
        html_content = html_content.replace('<head>', '<head>\n' + css_tag)
    
    return html_content


def process_html_file(file_path, navbar_html, navbar_css):
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject navbar
        content = inject_navbar_into_html(content, navbar_html)
        
        # Inject CSS
        content = inject_css_into_html(content, navbar_css)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Processed: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Inject SWHID unified navbar into HTML files')
    parser.add_argument('directory', help='Directory containing HTML files to process')
    parser.add_argument('--plugin-dir', help='Directory containing plugin files', 
                       default=os.path.join(os.path.dirname(__file__), '..', 'plugins'))
    parser.add_argument('--css-only', action='store_true', 
                       help='Only inject CSS, not the navbar HTML')
    parser.add_argument('--html-only', action='store_true', 
                       help='Only inject navbar HTML, not CSS')
    
    args = parser.parse_args()
    
    # Load navbar content
    navbar_html = None
    navbar_css = None
    
    if not args.css_only:
        navbar_html = load_navbar_html(args.plugin_dir)
        if not navbar_html:
            print(f"Warning: Could not load navbar HTML from {args.plugin_dir}")
    
    if not args.html_only:
        navbar_css = load_navbar_css(args.plugin_dir)
        if not navbar_css:
            print(f"Warning: Could not load navbar CSS from {args.plugin_dir}")
    
    if not navbar_html and not navbar_css:
        print("Error: No navbar content to inject")
        sys.exit(1)
    
    # Process HTML files
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    html_files = list(directory.rglob('*.html'))
    if not html_files:
        print(f"Warning: No HTML files found in {directory}")
        return
    
    print(f"Processing {len(html_files)} HTML files in {directory}")
    
    success_count = 0
    for html_file in html_files:
        if process_html_file(html_file, navbar_html, navbar_css):
            success_count += 1
    
    print(f"\nCompleted: {success_count}/{len(html_files)} files processed successfully")


if __name__ == '__main__':
    main()
