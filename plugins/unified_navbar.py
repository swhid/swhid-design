"""
SWHID Unified Navbar Plugin for MkDocs

This plugin injects the unified SWHID navigation bar into MkDocs sites
to provide consistent navigation across the main site, specification, and governance.
"""

import os
import re
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File


class UnifiedNavbarPlugin(BasePlugin):
    """Plugin to inject unified SWHID navigation bar into MkDocs sites."""
    
    config_scheme = (
        ('navbar_html', config_options.Type(str, default='')),
        ('navbar_css', config_options.Type(str, default='')),
        ('site_type', config_options.Type(str, default='specification')),
    )
    
    def __init__(self):
        super().__init__()
        self.navbar_html = None
        self.navbar_css = None
    
    def on_config(self, config, **kwargs):
        """Initialize the plugin with navbar content."""
        # Get the plugin directory
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load navbar HTML
        navbar_file = os.path.join(plugin_dir, 'unified-navbar.html')
        if os.path.exists(navbar_file):
            with open(navbar_file, 'r', encoding='utf-8') as f:
                self.navbar_html = f.read()
        
        # Load navbar CSS
        css_file = os.path.join(plugin_dir, 'unified-navbar.css')
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                self.navbar_css = f.read()
        
        # Add CSS to extra_css if not already present
        if self.navbar_css and 'unified-navbar.css' not in str(config.get('extra_css', [])):
            config['extra_css'] = config.get('extra_css', []) + ['unified-navbar.css']
        
        return config
    
    def on_post_template(self, template_content, template_name, config, **kwargs):
        """Inject the unified navbar into the full HTML template."""
        if not self.navbar_html:
            return template_content
        
        # Only process HTML templates, skip XML and other non-HTML templates
        if not template_name.endswith('.html'):
            return template_content
        
        # Determine the site type from the config
        site_type = self.config.get('site_type', 'specification')
        
        # Create the navbar HTML with proper site type
        navbar_html = self._create_navbar_html(site_type)
        
        # Inject the navbar after the opening body tag
        body_pattern = r'(<body[^>]*>)'
        match = re.search(body_pattern, template_content)
        if match:
            template_content = re.sub(body_pattern, r'\1\n' + navbar_html, template_content, count=1)
        else:
            # Fallback: inject after <body> tag
            template_content = template_content.replace('<body>', '<body>\n' + navbar_html, 1)
        
        return template_content
    
    
    def on_post_page(self, output, page, config, **kwargs):
        """Inject navbar into individual pages after they are rendered."""
        if not self.navbar_html:
            return output
        
        # Determine the site type from the config
        site_type = self.config.get('site_type', 'specification')
        
        # Create the navbar HTML with proper site type
        navbar_html = self._create_navbar_html(site_type)
        
        # Inject the navbar after the opening body tag
        body_pattern = r'(<body[^>]*>)'
        match = re.search(body_pattern, output)
        if match:
            output = re.sub(body_pattern, r'\1\n' + navbar_html, output, count=1)
        
        return output
    
    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        """Add CSS content to the page if needed."""
        if not self.navbar_css:
            return markdown
        
        # This is a fallback - CSS should be handled by extra_css
        return markdown
    
    def _create_navbar_html(self, site_type):
        """Create the navbar HTML with proper active state."""
        if not self.navbar_html:
            return ""
        
        # Create a simple navbar without active state logic for now
        # as requested by the user
        navbar = self.navbar_html
        
        # Replace any placeholders if needed
        navbar = navbar.replace('{{site_type}}', site_type)
        
        return navbar
