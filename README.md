# Commerce
### Project 2


## Overview
An e-commerce auction platform inspired by eBay, built with Django. Users can create listings, place bids, comment, and manage a personalized watchlist.


## Features

1. User Authentication

* Register, login, and logout functionality
* Personalized experience for each user

2. Create Listings

* Users can create auction listings with:
  - Title
  - Description
  - Starting bid
  - Optional image URL
  - Optional category

3. Active Listings

* Homepage displays all active listings
* Each listing shows:
  - Title
  - Description
  - Current price
  - Image (if provided)

4. Listing Page

* View full details of a listing
* Place bids (must be higher than current bid)
* Add/remove from watchlist
* Add comments

5. Bidding System
* Validates bids (must exceed current highest bid)
* Updates listing price dynamically
* Handles invalid bid feedback

6. Watchlist

* Users can add/remove listings
* Dedicated page to view saved listings

7. Comments

* Users can post comments on listings
* All comments are displayed on the listing page

8. Categories

* Listings can be grouped by category
* Users can browse listings by category

9. Close Auction

* Listing owner can close the auction
* Highest bidder is declared the winner
* Listing becomes inactive

10. Admin Panel

* Admin can manage:
  - Listings
  - Bids
  - Comments


## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite (default Django DB)


## Key Concepts

* Django models and relational data design (Listings, Bids, Comments, Users)
* Handling user authentication and session management
* Form validation and server-side logic
* Managing state (active vs closed listings)
* Dynamic updates based on user interactions


## How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/AA24107/CS50W-Commerce
   cd commerce
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the server:

   ```bash
   python manage.py runserver


## Demo

[![Watch the demo](https://img.youtube.com/vi/HN7HNwUHNg8/0.jpg)](https://youtu.be/HN7HNwUHNg8)