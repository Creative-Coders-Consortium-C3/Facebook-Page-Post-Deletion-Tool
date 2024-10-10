# Facebook Post Deletion Tool

This tool allows users to bulk delete Facebook posts from their pages based on various filters. It provides a command-line interface for authenticating, selecting pages, loading posts, and applying deletion filters.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Parameters and Filters](#parameters-and-filters)
- [Running in Google Colab](#running-in-google-colab)
- [Important Notes](#important-notes)
- [Contributing](#contributing)
- [License](#license)

## Features

- Authenticate with Facebook using a user access token
- List and select Facebook pages
- Load posts from selected pages
- Apply filters to posts before deletion:
  - Date range
  - Post type (photo, video, status, link)
  - Reaction threshold
- Bulk delete filtered posts
- Logging of operations and error handling

## Requirements

- Python 3.6+
- `requests` library
- `python-dateutil` library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/facebook-post-deletion-tool.git
   cd facebook-post-deletion-tool
   ```

2. Install the required libraries:
   ```
   pip install requests python-dateutil
   ```

## Usage

1. Obtain a Facebook User Access Token with the necessary permissions (manage_pages, publish_pages).

2. Run the script:
   ```
   python facebook_post_deletion_tool.py
   ```

3. Follow the prompts to:
   - Enter your Facebook User Access Token
   - Select a page
   - Choose to load all posts or a specific number
   - Apply filters (date range, post type, reaction threshold)
   - Confirm deletion

## Parameters and Filters

### User Access Token
- Required for authentication
- Must have `pages_show_list`,`pages_read_user_content`,`pages_manage_posts`,`pages_manage_engagement`  and `pages_read_engagement` permissions

### Page Selection
- Choose from a list of pages you manage

### Post Loading
- Option to load all posts or specify a limit

### Filters
1. **Date Range**
   - Start date (YYYY-MM-DD)
   - End date (YYYY-MM-DD)

2. **Post Type**
   - Options: photo, video, status, link, all

3. **Reaction Threshold**
   - Minimum number of reactions to keep a post

## Running in Google Colab

To run this script in Google Colab, click the button below to open the pre-existing notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1x7M-DZLPdpyKCHv_i620mBi_Jk18xJWO?usp=sharing)

Once the notebook is open:

1. Click on "Copy to Drive" to create your own editable copy

2. In the first code cell, install the required libraries:
   ```python
   !pip install requests python-dateutil
   ```

3. Copy the content of `facebook_post_deletion_tool.py` into a new code cell

4. Run the cell to define the `FacebookPostDeletionTool` class and the `main()` function

5. In a new cell, call the `main()` function:
   ```python
   if __name__ == "__main__":
       main()
   ```

6. Run this cell and follow the prompts in the output to use the tool

Note: You'll need to enter your Facebook User Access Token in the Colab environment. Ensure you're using a secure, private session and remove the token when you're done.

## Important Notes

- This tool permanently deletes posts. Use with caution and consider backing up your data before use.
- Respect Facebook's API usage limits to avoid being rate-limited or blocked.
- Keep your access token secure and do not share it with others.
- This tool does not delete posts marked as "profile picture updates" to prevent unintended profile changes.

## Contributing

Contributions to improve the tool are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
