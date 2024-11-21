### Product API:

This is the Backend for Product API
## Instruction:

how to run on local:

please install docker desktop or docker daemon before running the below commands

1) Docker:
- Clone the repo
- Run ```docker build -t praduyot-dailyrounds .```
- Run ```docker run -p 8000:8000 praduyot-dailyrounds```

to run the test cases 
- Run ```PYTHONPATH=. pytest```


## Postman Link:
https://www.postman.com/ps1357/workspace/praduyot/collection/12965729-dfed8f4e-c3fc-4ddf-a033-d62419cf7482?action=share&creator=12965729


## Design Decisions:

Reasoning behind the decisions I have taken to make the database schema design: I have added both the review and product in the same collection and made the reviews as a list, many would think this may not be that well for scalabilty but in most websites even like Myntra, Zomato reviews are not more than 200(at max) so it should be pretty scalable and plus if I had made different collections keeping in mind the scalabilty then MongoDB would have been a terrible choice because it would create too many relations and would instead scale down the scalabilty of the app. Also I have made a clear schema for the reviews because the likliness of the review schema changing is very low. I have added the user in a dictionary in memory and taking it as the db for easier authentication and authorization. 
