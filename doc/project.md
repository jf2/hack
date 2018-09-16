## Inspiration
Whether you are a private person or a business, you will encounter the situation in life where you want to know more about a place. Be it for a business venture or even to determine a future place to live in. 

## What it does
Our tool mundoris provides you vast information related to risks. Given risk factors ranging from natural hazards, political stability to economic outlook, our algorithm calculates a risk score associated to a location. 
The main user interface shows you an overall risk score overlaid on the map of the world - directly providing an overview of the visible region.
By selecting a location through the map or the search bar, detailed risk factors are shown to the user.

## How we built it
The prototype is a web-based application. 
In the backend, it accesses the datasets of the Google Earth Engine (various satellite imagery) and other data provides such as usgs.com to aggregate information about a location.
It is automatically delivered and updated via Continuous Deployment using Travis Kubernetes and Google Cloud platform.

## Challenges we ran into
Staying aligned to the Google Earth Engine API for dataset analysis and Google Maps seemed like an efficient decision, but cost us flexibility to choose another solution when hit limitations of these solutions.   

## Accomplishments that we're proud of
We enjoyed to find and aggregate data available online and deliver a new experience in risk analysis.

## What we learned
You cannot rely on proper API documentation. 
GUI tweaking can consume a lot of time - which you lack during a hackathon.
There is lots of data out there; what you need is to find ways to parse, interpret and extract the essential information of it. 

## What's next for mundoris
Scale it up! The plugin-like structure allows to easily extend the application with more risk components. 