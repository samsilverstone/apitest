APITEST


Getting Started
1. Download the the project.
2. After extracting the file, change the name of the main directory to apitest from apitest-master.
3. Run requirements.txt file using this command 'pip install -r requirements.txt' in your shell.
4. When all the required modules have been downloaded, open your postgresql and make two databases one for test and one for production        and store their names in env file at TEST_DB_NAME and DB_NAME respectively and fill the rest of the other details accordingly.
5. After this, run the test cases by using 'pytest' command.
5. After we are done with testing, we can run the server using this command 'python run.py' and can interact with the API by using      postman.

Postman
1. Structure for /post_location (json format)

{
	"pin":"IN/110067",
	"Latitude":"27.208",
	"Longitude":"8.013426",
	"address":"Khanpur",
	"city": "New Delhi",
	"accuracy": "4"
}

2. Structure for /get_using_self (json format)
{
	"Latitude":"28.597",
	"Longitude":"77.212",
	"Value":5 #(kms)
	
}

3. Structure for /get_using_postgres (json format)
{
	"Latitude":"28.597",
	"Longitude":"77.212",
	"Value":5 #(kms)
	
}

4. Structure for /latitude_longitude (json format)

{
	"Latitude":"28.597",
	"Longitude":"77.212"
}
