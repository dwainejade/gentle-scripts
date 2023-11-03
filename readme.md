# Gentle Readalong Script

This repository contains a Python script designed to work with the Gentle forced aligner to create JSON files with accurate word timings for use in readalong applications.

## Prerequisites

Before you begin, make sure you have the following:

- Gentle forced aligner running locally on your machine.
- Python 3.6 or higher.
- A directory containing an audio folder and a corresponding Excel file. The directory and the Excel file should have the same name.

## Gentle Setup

1. Install Gentle from its [official repository](https://github.com/lowerquality/gentle).
2. Follow the installation instructions to set up Gentle on your computer.
3. Run Gentle. Note the port it is running on, as you will need this for the script.

## Installation

To set up the Readalong Script, follow these steps:

## Usage

1. Ensure Gentle is running and note the port number.
2. Place your audio files in an /audio directory within a folder named after your project.
3. Ensure that an Excel file with the same name as your project folder is present in the folder.
4. Run the script with: `python3 main.py`
5. When prompted, enter the full path to your project folder.
6. When prompted, enter the port number that Gentle is running on.
7. The script will process the audio and text, then generate a JSON file with timings in your project folder.
