# FoodFast - Multi-Feature Flask Project

## Company Background

**FoodFast** is a food delivery platform serving 10,000 active users across 5 cities. The platform is experiencing rapid growth and aims to implement new features to stay competitive. FoodFast connects customers, restaurants, and delivery drivers through a mobile app and web platform.

This repository contains multiple independent Flask projects (features) within a single main project folder. Each feature can be run separately and independently.

---

## Features

- `feature1` - Example: User authentication and profiles
- `feature2` - Example: Restaurant management
- `feature7` - Image upload and processing services (requires background services)

---

## Prerequisites

- Python 3.8+
- `pip` installed

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all requirements:

```bash
pip install -r requirements.txt
```

```bash

Each feature can be run independently:
# Feature 1
python3 -m feature1.app

# Feature 2
python3 -m feature2.app

# Feature 7
# Start background services first
python3 -m feature7.quality_service &
python3 -m feature7.resize_compress_service &

# Then run the main app
python3 -m feature7.app
```
