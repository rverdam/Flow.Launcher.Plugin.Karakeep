# Karakeep Plugin

Karakeep is a FlowLauncher plugin that allows you to search for bookmarks stored in the Karakeep application. This plugin provides a quick and easy way to access your saved bookmarks directly from the FlowLauncher interface.

## Installation

You can install this plugin via the FlowLauncher plugin manager with the following command:

```
pm install Karakeep
```

## Configuration

Before you can use this plugin, you will need to configure it with your local Karakeep instance's base URL and API key. You can do this by setting the following two values in the plugin's settings:

- `Karakeep Base Address`: This is the base URL of your local Karakeep instance. For example, if you run Karakeep on http://localhost:8080, then this should be set to `http://localhost:8080`.

- `Karakeep API Key`: This is the API key that allows the plugin to search and open your Karakeep bookmarks. You can obtain this key from the Karakeep web interface by going to your profile settings > User Settings > API Keys page and clicking on "New API Key".

### API key permissions

The plugin only calls `GET /api/v1/bookmarks/search`, so the minimum Karakeep API key scope is:

- `bookmarks:read`

A key with `bookmarks:readwrite` or `fullaccess` will also work, but is not required. Prefer `bookmarks:read` for day-to-day use because the plugin does not create, edit, or delete bookmarks.

## Usage

Once installed, you can activate the Karakeep plugin by using the default action keyword `ka`. Simply type `ka` followed by your search query to find matching bookmarks stored in Karakeep.

### Example

To search for a bookmark related to "Python", you would use the following command in FlowLauncher:

```
ka Python
```

## Features

- **Quick Search**: Instantly search through your Karakeep bookmarks and notes (only contents).
- **Easy Access**: Open bookmarks and notes directly from FlowLauncher and copy notes contents.
- **Context Menu**: Access additional options using the context menu.

## Context Menu

The plugin provides a context menu option:

- **Copy URL to clipboard**: Copies the URL of the selected item to the clipboard.
- **Copy Note Text to clipboard**: Copies the content of the note to the clipboard.

## Development

This plugin is developed using Python and leverages the FlowLauncher API to integrate seamlessly with the FlowLauncher platform.

## Author

Karakeep Plugin is developed by Robert Verdam. You can find more about this plugin and contribute to its development on [GitHub](https://github.com/rverdam/Flow.Launcher.Plugin.Karakeep).

## License

This project is licensed under the MIT License.

---
