LoGAN:
loGAN is a React app made for generating logos for brands.

The steps for loGAN:
1) scrape the web for logos and industries of brands which have logos
2) take in a brand name and industry in frontend
3) create a database of brand names that are similar to the brand name input and brands that share the same industry
4) create an array of image data of logos from brands of previous database by pulling images from s3 bucket
5) run loGAN using array created above
6) display images on frontend
7) allow user to download an image, and save any downloaded images to an s3 bucket
8) display all previously downloaded images in gallery

Notes on files:
    data folder:
        cleanup.py: There was a unique problem with the data I scraped for industry. It came in wierd formats, sometimes with punctuation. Often there were multiple industries listed. This code is made to simplify the scraped data. cleanup.py also creates a new databse to hold the cleaned data.
        logn2.db: My database of brand name and industry. I used an s3 bucket to hold all the logos associated with the brand names. Because I saved the images with the same name as the brands, it was easy to pull from the database and find the corresponding images.
        schema.py: Creates the original logan.db file. logan.db is used in the data gathering.
    
    Web folder:
        aws.py: Contains everything I used to create an s3 bucket, and store images inside.
        scraper.py: My data scraper for both getting logos and getting industries
    
    Website folder:
        backend folder:
            routes.py: ROutes to tie the backend to the frontend.
             