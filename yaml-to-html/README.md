# YAML to Swagger HTML Converter

Convert Swagger/OpenAPI YAML files to interactive HTML documentation with a modern UI.

## Features

- ✨ Modern, responsive Swagger UI-like design
- 🎨 Color-coded HTTP methods (GET, POST, PUT, DELETE, PATCH)
- 📱 Expandable/collapsible sections for endpoints, requests, and responses
- 🎯 Status code highlighting (2xx green, 4xx orange, 5xx red)
- 📦 Data models with type information
- 🔍 Parameter tables with required/optional badges
- 💻 No external dependencies except PyYAML

## Installation

Install the required dependency:

```bash
pip install pyyaml
```

## Usage

### Basic Usage

```bash
python yaml_to_swagger_html.py input.yaml -o output.html
```

### Examples

Convert API specification:
```bash
python yaml_to_swagger_html.py PayInPartsApi-additional.yaml -o PayInPartsApi.html
```

Convert to a specific directory:
```bash
python yaml_to_swagger_html.py api.yaml -o docs/api-documentation.html
```

### Command Line Options

- `input` - Path to the input YAML file (required)
- `-o`, `--output` - Path to the output HTML file (required)

## Features in Generated HTML

### Interactive Elements

1. **Endpoint Cards** - Click to expand/collapse entire endpoint details
2. **Request Sections** - Collapsible request parameters and examples
3. **Response Sections** - Individual collapsible response status codes
4. **Data Models** - Expandable model definitions with field tables

### Color Coding

- **GET** - Blue badge
- **POST** - Green badge
- **PUT** - Orange badge
- **DELETE** - Red badge
- **PATCH** - Purple badge

### Status Codes

- **2xx** (Success) - Green background
- **4xx** (Client Error) - Orange background
- **5xx** (Server Error) - Red background

## Supported Swagger/OpenAPI Features

- ✅ Swagger 2.0 specifications
- ✅ Info (title, version, description)
- ✅ Base path and schemes
- ✅ All HTTP methods
- ✅ Path parameters
- ✅ Query parameters
- ✅ Body parameters with schema references
- ✅ Response definitions
- ✅ Data models/definitions
- ✅ Enum types
- ✅ Array types
- ✅ Required/optional fields
- ✅ Tags for endpoint grouping

## Example Output

The generated HTML includes:

1. **Header Section**
   - API title and version
   - Base path and supported schemes
   - Description

2. **Endpoints Section**
   - All API endpoints organized by path
   - HTTP method badges
   - Tags for categorization
   - Request parameters
   - Response definitions

3. **Data Models Section**
   - Object definitions
   - Enum definitions
   - Field types and descriptions
   - Required field indicators

## Requirements

- Python 3.6+
- PyYAML

## Notes

- The output HTML is self-contained (no external CSS/JS dependencies)
- Works with any Markdown/HTML preview tool
- Can be opened directly in web browsers
- Responsive design works on mobile devices

## License

Free to use and modify.
