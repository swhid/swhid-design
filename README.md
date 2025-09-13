# SWHID Design System

A minimal, framework-agnostic design system for the SWHID project that provides consistent branding across Jekyll and MkDocs sites.

## Structure

```
swhid-design/
├── css/
│   ├── tokens.css         # CSS variables: colors, layout, typography
│   └── swhid-brand.css    # base links, topbar, footer styles
└── partials/
    ├── header.html        # slim global header/topbar
    └── footer.html        # unified footer
```

## Usage

### Jekyll (swhid.github.io)
- Copy CSS files to `assets/design/`
- Include in `_sass/custom/custom.scss`
- Copy partials to `_includes/components/`

### MkDocs (specification, governance)
- Copy CSS files to `docs/assets/design/`
- Reference in `mkdocs.yml` via `extra_css`
- Use partials in theme overrides

## Design Tokens

- **Red**: #e20026 (primary brand color)
- **Orange**: #ef4426 (accent color)
- **Light Orange**: #f79622
- **Yellow**: #fabf1f
- **Grey**: #737373 (muted text)

## Version

v0.1.0 - Initial release with basic branding and layout components
