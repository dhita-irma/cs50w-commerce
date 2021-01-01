# Commerce
Simple auction website built with Django 

## Table of Contents
- [Project Summary](#project-summary)
- [Technologies](#technologies)
- [Features](#features)
- [Setup](#setup)
- [Sources](#sources)


## Project Summary
This project is created for [Project 2 of CS50W](https://cs50.harvard.edu/web/2020/projects/2/commerce/). Commerce is an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Technologies 
This project is created with Python Django 3.1

Library: django-crispy-forms v1.9.2 is used to style forms in Django

## Features 
- **Create Listing**: User can specify a title for the listing, a text-based description, and what the starting bid should be. Users would also optionally be able to provide a URL for an image for the listing and/or a category.
- **Listing Page**: Clicking on a listing would take users to a page specific to that listing. This page displays all the details about the listing, including the current price.
- **Watchlist**: User can click a button to add an item to their "Watchlist" and click the button again to remove it. 
- **Make Bid**: If user is logged in, they can place a bid on the item. If the bid is lower than the current price, they would be presented with an error message. 
- **Close Auction**: If the user is signed in and is the one who created the listing, the user would have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
- **Winning Alert**: If a user is signed in on a closed listing page, and the user has won that auction, the page would say so.
- **Add Comments**: Users who are signed in can add comments to the listing page. The listing page would display all comments that have been made on the listing.
- **Categories**: Users can visit a page that displays a list of all listing categories. Clicking on the name of any category would take the user to a page that displays all of the active listings in that category.


## Setup 
- Clone or download this repository in the folder and open it in your editor of choice.
- Create and activate [virtual environment](https://docs.python.org/3.9/library/venv.html) by running following command in the terminal of the base directory of this project:

    ```
    python -m venv <virtual environment name>
    C:\> <venv address>\Scripts\activate
    ```

- Then install the project dependencies with
    ```
    pip install -r requirements.txt
    ```
- Now you can run the project with this command
    ```
    python manage.py runserver

    ```

## Sources 
The listings in the database of this project is taken from [Catawiki](https://www.catawiki.com/)
