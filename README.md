# Albion Crafting Calculator

> **⚠️ OUTDATE NOTICE**  
> This documentation may be outdated. Please check the latest version for accurate information.

## Overview
A desktop application for Albion Online crafting profit calculations with updated fame values and journal calculations.

## Features
- Resource cost calculation (up to 3 resources)
- Automatic fame calculation based on:
  - Item tier (T4-T8)
  - Item type (Helmet, Shoes, etc)
- Journal profit integration
  - Auto-fills empty journal fame based on tier
  - Calculates journal completion ratio
- Tax and RRR calculations

## Installation
1. Install Python 3.12 or newer
2. Install dependencies:
```
pip install -r requirements.txt
```

## Running
### Development
```
python albion_craft_gui.py
```

### Create Executable
```
python -m auto_py_to_exe
```
Select:
- Script: albion_craft_gui.py
- One File
- Window Based

## Project Structure
```
albion-crafting-calculator/
├── albion_craft_gui.py   # Main application
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```