![CI badge](https://github.com/cegonse/backend-challenge-vlc/workflows/Python%20package/badge.svg)

# Summary

Total time from start to finish: around 3 hours.

Some of the details of my implementation of the backend challenge:
* I've opted to do a fresh start on my code, basing the classes from the boostrap code. These classes have helped me have a better
  overall picture of the domain, which I have tried to express in the diagram below.
* The first step was setting up the CI pipeline for the project, and defining the requirements as user stories. I've opted to use
  the [Minimum Value Increments](https://www.codurance.com/publications/2020/01/27/minimum-valuable-increment), a framework proposed by the people at Codurance to define value which I find really interesting
  and have been trying to use lately.
* For all classes, I've used named arguments instead of attribute dicts. This was just due to personal preference.
* Processing payments of orders with different types of items is supported. I have assumed the different requirements are not contradicting themselves.
  For example, in case you purchase a physical item and a digital media item, you will be charged with the total sum and receive the corresponding parcel
  for the physical item (shipping label) and the emails associated to the digital media item (discount voucher and confirmation).
* I have assumed the tax exemption on the books is a shipping issue. At first, I thought it should be part of the payment. For example, if you purchase
  a mobile phone and a book, you would be charged 21% VAT for the mobile phone and 0% VAT for the book, affecting the total sum. But in the end, since the
  requirement only mentioned the shipping label I kept it like that.
* I have recorded all the session as a YouTube video, so you can hear first hand what's behind the decisions I've taken to solve each user story.
  The reason why I've decided to do this is because during the technical interviews I've been able to do to other candidates, being able to speak with them
  and hear their reasoning while they were conducting the challenge was really enlightning to better understand their thought process. Sadly, we cannot do
  this now due to COVID but I think this might be quite close.

# Model diagram

![Model diagram](media/domain_model.png?raw=true)

# YouTube Video

*Uploading!*

# Running the project

The requirements to run the project are:
* Python 3.7+
* Pytest

To run the unit tests, run in a terminal:
```
pytest .
```
