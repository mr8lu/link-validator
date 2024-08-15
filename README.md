# link-validator
Github Action for validating Markdown and Jupyter Notebook links

![GitHub release (latest by date)](https://img.shields.io/github/v/release/mr8lu/link-validator)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mr8lu/link-validator/example-usage.yml)

## Overview

This GitHub Action checks for broken links in Markdown files and Jupyter Notebooks. It can be used in any repository to automatically validate the links during your CI/CD process, ensuring that all links in your documentation are valid.

## Features

- **Markdown Support:** Validate links in `.md` files.
- **Jupyter Notebook Support:** Validate links in `.ipynb` files.
- **Handles Markdown and HTML Links:** Supports both Markdown-style and HTML-style links within Markdown and Notebook cells.
- **Optional Authentication:** Optionally use a GitHub Personal Access Token (PAT) to validate links in private repositories.

## Inputs

- `PAT_TOKEN` (optional): GitHub Personal Access Token (PAT) for accessing private repositories.
  - **Type:** `string`
  - **Required:** `false`
  - **Default:** `None`
  
- `directory` (required): The directory to search for Markdown and Notebook files.
  - **Type:** `string`
  - **Required:** `true`
  - **Default:** `.` (current directory)

## Outputs

- `broken_links_found`: Indicates if any broken links were found.
  - **Type:** `boolean`

## Usage

You can use this action in your workflow file (e.g., `.github/workflows/link-check.yml`):

```yaml
name: Link Checker

on: [push, pull_request]

jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Run Link Checker
        uses: mr8lu/link-validator@v1
        with:
          PAT_TOKEN: ${{ secrets.PAT_TOKEN }}  # Optional
          directory: '.'  # Adjust the directory as needed
```
