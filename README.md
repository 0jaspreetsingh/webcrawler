# Python Web Crawler using Scrapy

This project implements a web crawler in Python using the Scrapy framework. The crawler is designed to extract data from specific websites.

## Setup

To set up the project, follow these steps:

1. Create a new Conda environment using the provided `requirements.txt` file. Execute the following command: `conda create --name <env> --file requirements.txt`


## Usage

To run the web crawler, perform the following steps:

1. Navigate to the `colombus` directory in the terminal.
2. Execute the command below to crawl the website [https://www.uvp-verbund.de/freitextsuche?rstart=0&currentSelectorPage=1](https://www.uvp-verbund.de/freitextsuche?rstart=0&currentSelectorPage=1): `scrapy crawl uvp`
3. Execute the command below to crawl the website [http://sthjj.pds.gov.cn/channels/11330.html](http://sthjj.pds.gov.cn/channels/11330.html): `scrapy crawl sthjj`


Make sure to replace `<env>` with the desired name for your Conda environment.

## Contributing

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvement, please submit a pull request or open an issue on the GitHub repository.
