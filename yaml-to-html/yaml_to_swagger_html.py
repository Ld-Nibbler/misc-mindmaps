#!/usr/bin/env python3
"""
Swagger/OpenAPI YAML to Interactive HTML Converter

Usage:
    python yaml_to_swagger_html.py input.yaml -o output.html
"""

import yaml
import argparse
import sys
from pathlib import Path


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background: #f8fafc;
  }}
  .container {{
    max-width: 1200px;
    margin: 0 auto;
  }}
  .api-header {{
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 30px;
    border-radius: 8px;
    margin-bottom: 30px;
  }}
  .api-header h1 {{
    margin: 0;
    font-size: 2.5em;
  }}
  .api-info {{
    margin-top: 10px;
    opacity: 0.9;
  }}
  .api-info code {{
    background: rgba(255,255,255,0.2);
    padding: 2px 6px;
    border-radius: 3px;
  }}
  .section-header {{
    font-size: 1.8em;
    color: #1e293b;
    margin: 30px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #3b82f6;
  }}
  .endpoint {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-bottom: 20px;
    overflow: hidden;
  }}
  .endpoint-header {{
    background: white;
    padding: 15px 20px;
    border-bottom: 1px solid #e2e8f0;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 15px;
    transition: background 0.2s;
  }}
  .endpoint-header:hover {{
    background: #f9fafb;
  }}
  .method-badge {{
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.85em;
    text-transform: uppercase;
    min-width: 60px;
    text-align: center;
  }}
  .method-post {{
    background: #10b981;
    color: white;
  }}
  .method-get {{
    background: #3b82f6;
    color: white;
  }}
  .method-put {{
    background: #f59e0b;
    color: white;
  }}
  .method-delete {{
    background: #ef4444;
    color: white;
  }}
  .method-patch {{
    background: #8b5cf6;
    color: white;
  }}
  .endpoint-path {{
    font-family: 'Courier New', monospace;
    font-size: 1.1em;
    color: #1e293b;
    flex: 1;
  }}
  .endpoint-tag {{
    background: #e0e7ff;
    color: #4338ca;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.85em;
  }}
  .expand-icon {{
    transition: transform 0.3s;
    font-size: 1.2em;
    color: #64748b;
  }}
  .expand-icon.expanded {{
    transform: rotate(180deg);
  }}
  .endpoint-body {{
    padding: 20px;
    display: none;
  }}
  .endpoint-body.show {{
    display: block;
  }}
  .endpoint-description {{
    background: #fff;
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 20px;
    border-left: 4px solid #3b82f6;
  }}
  .section-title {{
    color: #1e293b;
    font-size: 1.2em;
    font-weight: 600;
    margin: 20px 0 10px 0;
    padding-bottom: 5px;
    border-bottom: 2px solid #e2e8f0;
  }}
  .collapsible-section {{
    margin: 15px 0;
  }}
  .collapsible-header {{
    background: #f8fafc;
    padding: 10px 15px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    color: #1e293b;
    transition: background 0.2s;
    border: 1px solid #e2e8f0;
  }}
  .collapsible-header:hover {{
    background: #f1f5f9;
  }}
  .collapsible-content {{
    margin-top: 10px;
    display: none;
  }}
  .collapsible-content.show {{
    display: block;
  }}
  .param-table, .response-table {{
    width: 100%;
    background: white;
    border-collapse: collapse;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 10px 0;
  }}
  .param-table th, .response-table th {{
    background: #f1f5f9;
    padding: 12px;
    text-align: left;
    font-weight: 600;
    color: #475569;
    border-bottom: 2px solid #e2e8f0;
  }}
  .param-table td, .response-table td {{
    padding: 12px;
    border-bottom: 1px solid #f1f5f9;
  }}
  .param-table tr:last-child td, .response-table tr:last-child td {{
    border-bottom: none;
  }}
  .param-type {{
    color: #7c3aed;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
  }}
  .required-badge {{
    background: #fee2e2;
    color: #991b1b;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75em;
    font-weight: 600;
  }}
  .optional-badge {{
    background: #f3f4f6;
    color: #6b7280;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75em;
  }}
  .response-status {{
    display: inline-block;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    margin: 5px 0;
  }}
  .status-200, .status-201, .status-204 {{
    background: #d1fae5;
    color: #065f46;
  }}
  .status-400, .status-401, .status-403 {{
    background: #fed7aa;
    color: #92400e;
  }}
  .status-404, .status-500, .status-502, .status-503 {{
    background: #fecaca;
    color: #991b1b;
  }}
  .code-block {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    margin: 10px 0;
    white-space: pre-wrap;
  }}
  .model-card {{
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    overflow: hidden;
  }}
  .model-header {{
    padding: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: background 0.2s;
  }}
  .model-header:hover {{
    background: #f9fafb;
  }}
  .model-title {{
    color: #1e293b;
    font-size: 1.3em;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .model-type-badge {{
    background: #ddd6fe;
    color: #5b21b6;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.7em;
    font-weight: 600;
  }}
  .model-body {{
    padding: 0 20px 20px 20px;
    display: none;
  }}
  .model-body.show {{
    display: block;
  }}
  .chevron {{
    color: #64748b;
    font-size: 0.9em;
  }}
  code {{
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
  }}
</style>
</head>
<body>
<div class="container">
{content}
</div>

<script>
function toggleEndpoint(header) {{
  const body = header.nextElementSibling;
  const icon = header.querySelector('.expand-icon');

  if (body.classList.contains('show')) {{
    body.classList.remove('show');
    icon.classList.remove('expanded');
  }} else {{
    body.classList.add('show');
    icon.classList.add('expanded');
  }}
}}

function toggleSection(header) {{
  const content = header.nextElementSibling;
  const chevron = header.querySelector('.chevron');

  if (content.classList.contains('show')) {{
    content.classList.remove('show');
    chevron.textContent = '▶';
  }} else {{
    content.classList.add('show');
    chevron.textContent = '▼';
  }}
}}

function toggleModel(header) {{
  const body = header.nextElementSibling;
  const icon = header.querySelector('.expand-icon');

  if (body.classList.contains('show')) {{
    body.classList.remove('show');
    icon.classList.remove('expanded');
  }} else {{
    body.classList.add('show');
    icon.classList.add('expanded');
  }}
}}
</script>
</body>
</html>
'''


def get_ref_name(ref_path):
    """Extract the definition name from a $ref path."""
    if isinstance(ref_path, dict) and '$ref' in ref_path:
        return ref_path['$ref'].split('/')[-1]
    return None


def format_type(param, definitions=None):
    """Format parameter type with enum information."""
    if '$ref' in param:
        ref_name = get_ref_name(param)
        return f'<span class="param-type">{ref_name}</span>'

    param_type = param.get('type', 'object')
    format_type = param.get('format', '')

    type_str = param_type
    if format_type:
        type_str += f' ({format_type})'

    if param.get('enum'):
        type_str += ' (enum)'

    if param_type == 'array' and 'items' in param:
        items = param['items']
        if '$ref' in items:
            ref_name = get_ref_name(items)
            type_str = f'array[{ref_name}]'
        else:
            items_type = items.get('type', 'object')
            type_str = f'array[{items_type}]'

    return f'<span class="param-type">{type_str}</span>'


def render_parameters(parameters, definitions=None):
    """Render parameters table."""
    if not parameters:
        return ""

    html = '<div class="section-title">Parameters</div>\n'
    html += '<table class="param-table">\n'
    html += '  <thead>\n    <tr>\n'
    html += '      <th>Parameter</th>\n      <th>In</th>\n      <th>Type</th>\n'
    html += '      <th>Required</th>\n      <th>Description</th>\n'
    html += '    </tr>\n  </thead>\n  <tbody>\n'

    for param in parameters:
        # Handle body parameters with schema
        if param.get('in') == 'body' and 'schema' in param:
            schema = param['schema']
            name = param.get('name', 'body')
            description = param.get('description', '')

            if '$ref' in schema:
                ref_name = get_ref_name(schema)
                type_str = f'<span class="param-type">{ref_name}</span>'
            else:
                type_str = format_type(schema, definitions)

            required = '<span class="required-badge">required</span>'

            html += f'    <tr>\n'
            html += f'      <td><code>{name}</code></td>\n'
            html += f'      <td>body</td>\n'
            html += f'      <td>{type_str}</td>\n'
            html += f'      <td>{required}</td>\n'
            html += f'      <td>{description}</td>\n'
            html += f'    </tr>\n'
        else:
            name = param.get('name', '')
            in_loc = param.get('in', '')
            description = param.get('description', '')
            required = param.get('required', False)

            type_str = format_type(param, definitions)
            required_badge = '<span class="required-badge">required</span>' if required else '<span class="optional-badge">optional</span>'

            html += f'    <tr>\n'
            html += f'      <td><code>{name}</code></td>\n'
            html += f'      <td>{in_loc}</td>\n'
            html += f'      <td>{type_str}</td>\n'
            html += f'      <td>{required_badge}</td>\n'
            html += f'      <td>{description}</td>\n'
            html += f'    </tr>\n'

    html += '  </tbody>\n</table>\n'
    return html


def render_responses(responses):
    """Render responses section."""
    html = '<div class="collapsible-section">\n'
    html += '  <div class="collapsible-header" onclick="toggleSection(this)">\n'
    html += '    <span class="chevron">▶</span>\n'
    html += '    <span>📤 Responses</span>\n'
    html += '  </div>\n'
    html += '  <div class="collapsible-content">\n\n'

    for status_code, response in responses.items():
        status_class = f"status-{status_code}"
        description = response.get('description', '')

        html += '<div class="collapsible-section">\n'
        html += '  <div class="collapsible-header" onclick="toggleSection(this)">\n'
        html += '    <span class="chevron">▶</span>\n'
        html += f'    <span class="response-status {status_class}">{status_code}</span>\n'
        html += '  </div>\n'
        html += '  <div class="collapsible-content">\n\n'

        if description:
            html += f'<p>{description}</p>\n\n'

        # Check for schema in response
        if 'schema' in response:
            schema = response['schema']
            if '$ref' in schema:
                ref_name = get_ref_name(schema)
                html += f'<p><strong>Response Model:</strong> <code>{ref_name}</code></p>\n'

        html += '  </div>\n</div>\n\n'

    html += '  </div>\n</div>\n\n'
    return html


def render_endpoint(path, method, operation, tag=None):
    """Render a single endpoint."""
    summary = operation.get('summary', '')
    description = operation.get('description', '')
    parameters = operation.get('parameters', [])
    responses = operation.get('responses', {})

    method_class = f"method-{method.lower()}"

    html = '<div class="endpoint">\n'
    html += '  <div class="endpoint-header" onclick="toggleEndpoint(this)">\n'
    html += f'    <span class="method-badge {method_class}">{method.upper()}</span>\n'
    html += f'    <span class="endpoint-path">{path}</span>\n'

    if tag:
        html += f'    <span class="endpoint-tag">{tag}</span>\n'

    html += '    <span class="expand-icon">▼</span>\n'
    html += '  </div>\n'
    html += '  <div class="endpoint-body">\n'

    # Description
    if summary or description:
        html += '    <div class="endpoint-description">\n'
        if summary:
            html += f'      <strong>{summary}</strong>\n'
        if description:
            html += f'      <p>{description}</p>\n'
        html += '    </div>\n\n'

    # Parameters
    if parameters:
        html += '<div class="collapsible-section">\n'
        html += '  <div class="collapsible-header" onclick="toggleSection(this)">\n'
        html += '    <span class="chevron">▶</span>\n'
        html += '    <span>📥 Request</span>\n'
        html += '  </div>\n'
        html += '  <div class="collapsible-content">\n\n'
        html += render_parameters(parameters)
        html += '  </div>\n</div>\n\n'

    # Responses
    if responses:
        html += render_responses(responses)

    html += '  </div>\n</div>\n\n'
    return html


def render_model(name, schema):
    """Render a data model/definition."""
    model_type = schema.get('type', 'object').upper()
    description = schema.get('description', '')
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])
    enum_values = schema.get('enum', [])

    html = '<div class="model-card">\n'
    html += '  <div class="model-header" onclick="toggleModel(this)">\n'
    html += '    <div class="model-title">\n'
    html += f'      <span>{name}</span>\n'
    html += f'      <span class="model-type-badge">{model_type}</span>\n'
    html += '    </div>\n'
    html += '    <span class="expand-icon">▼</span>\n'
    html += '  </div>\n'
    html += '  <div class="model-body">\n'

    if description:
        html += f'    <p><em>{description}</em></p>\n\n'

    # For enum types
    if enum_values:
        html += '    <table class="param-table">\n'
        html += '      <thead>\n        <tr>\n'
        html += '          <th>Value</th>\n          <th>Description</th>\n'
        html += '        </tr>\n      </thead>\n      <tbody>\n'

        for value in enum_values:
            html += f'        <tr>\n'
            html += f'          <td><code>{value}</code></td>\n'
            html += f'          <td></td>\n'
            html += f'        </tr>\n'

        html += '      </tbody>\n    </table>\n'

    # For object types with properties
    elif properties:
        html += '    <table class="param-table">\n'
        html += '      <thead>\n        <tr>\n'
        html += '          <th>Field</th>\n          <th>Type</th>\n'
        html += '          <th>Required</th>\n          <th>Description</th>\n'
        html += '        </tr>\n      </thead>\n      <tbody>\n'

        for prop_name, prop_schema in properties.items():
            prop_desc = prop_schema.get('description', '')
            is_required = prop_name in required_fields
            required_badge = '<span class="required-badge">required</span>' if is_required else '<span class="optional-badge">optional</span>'

            prop_type = format_type(prop_schema)

            html += f'        <tr>\n'
            html += f'          <td><code>{prop_name}</code></td>\n'
            html += f'          <td>{prop_type}</td>\n'
            html += f'          <td>{required_badge}</td>\n'
            html += f'          <td>{prop_desc}</td>\n'
            html += f'        </tr>\n'

        html += '      </tbody>\n    </table>\n'

    html += '  </div>\n</div>\n\n'
    return html


def convert_yaml_to_html(yaml_file, output_file):
    """Convert Swagger YAML to interactive HTML."""
    try:
        # Load YAML file
        with open(yaml_file, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)

        # Extract basic info
        info = spec.get('info', {})
        title = info.get('title', 'API Documentation')
        version = info.get('version', 'v1')
        description = info.get('description', '')
        base_path = spec.get('basePath', '/')
        schemes = ', '.join(spec.get('schemes', ['http'])).upper()

        # Build content
        content = '<div class="api-header">\n'
        content += f'  <h1>📘 {title}</h1>\n'
        content += '  <div class="api-info">\n'
        content += f'    <strong>Version:</strong> {version} |\n'
        content += f'    <strong>Base Path:</strong> <code>{base_path}</code> |\n'
        content += f'    <strong>Schemes:</strong> {schemes}\n'
        content += '  </div>\n'

        if description:
            content += f'  <p style="margin-top: 15px; opacity: 0.95;">{description}</p>\n'

        content += '</div>\n\n'

        # Endpoints section
        paths = spec.get('paths', {})
        if paths:
            content += '<h2 class="section-header">🔌 Endpoints</h2>\n\n'

            for path, methods in paths.items():
                for method, operation in methods.items():
                    if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                        tags = operation.get('tags', [])
                        tag = tags[0] if tags else None
                        content += render_endpoint(path, method, operation, tag)

        # Models/Definitions section
        definitions = spec.get('definitions', {})
        if definitions:
            content += '<h2 class="section-header">📦 Data Models</h2>\n\n'

            for def_name, def_schema in definitions.items():
                content += render_model(def_name, def_schema)

        # Generate final HTML
        html = HTML_TEMPLATE.format(title=title, content=content)

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[SUCCESS] Successfully converted {yaml_file} to {output_file}")
        return True

    except FileNotFoundError:
        print(f"[ERROR] File '{yaml_file}' not found")
        return False
    except yaml.YAMLError as e:
        print(f"[ERROR] Error parsing YAML file: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert Swagger/OpenAPI YAML files to interactive HTML documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python yaml_to_swagger_html.py api.yaml -o api.html
  python yaml_to_swagger_html.py swagger.yaml -o docs/api-docs.html
        '''
    )

    parser.add_argument('input', help='Input YAML file path')
    parser.add_argument('-o', '--output', required=True, help='Output HTML file path')

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] Input file '{args.input}' does not exist")
        sys.exit(1)

    if not input_path.suffix.lower() in ['.yaml', '.yml']:
        print(f"[WARNING] Input file does not have .yaml or .yml extension")

    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert
    success = convert_yaml_to_html(args.input, args.output)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
