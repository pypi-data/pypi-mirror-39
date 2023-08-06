**Multi-Agent Accelerator for Data Science (MAADS)**

*Revolutionizing Data Science with Artificial Intelligence*

**Overview**

*MAADS combines Artificial Intelligence, Machine Learning and Natural Language Processing (with data engineering task automation) in one easy to use library, that allows clients to connect to the MAADS server located anywhere in the world and perform advanced analytics and embed intelligence in their organization seamlessly and fast!*

This library allows users to harness the power of agent-based computing using hundreds of advanced linear and non-linear algorithms. Users can easily integrate Predictive Analytics in any solution by wrapping additional code around the functions below. The system can:

- Automatically analyse your data and perform feature selection to determine which variables are more important than others.
- Automatically model your data for seasonality *Winter, Shoulder, and Summer seasons.*
- Automatically clean your data for outliers.
- Automatically make predictions using the BEST algorithm (out of hundreds of advanced algorithms) that best model your data.
- Perform *Natural Language Processing (NLP)* on large amounts of text data - and get MAADS to summarize the text. 
  For example, you can tell it to scrape a website, read a PDF, or text data and it will 
  return a concise summary.  This summary can be used to refine your modeling and give users  
  an integrated view of their business from a TEXT and ADVANCED ANALYTIC perspective.     
- Do all this in minutes.

To install this library a request should be made to the system administrator **sebastian.maurice@otics.ml** for a username and password.  Once you have these credentials then install this Python library.

**Compatibility**
    - Python 3.5 or greater
    - Minimal Python skills needed

**License**
   - Author: Sebastian Maurice, PhD
   - Copyright Sebastian Maurice (2018)
   - Commercial users please contact Sebastian Maurice (www.otics.ml, OTICS Advanced Analytics Inc.)

**Installation**
   - At the command prompt write:
     **pip install maads**
     - This assumes you have [Downloaded Python](https://www.python.org/downloads/) and installed it on your computer.  

**Syntax**
  - There are literally two lines of code you need to write to train your data and make predictions:

**Main functions:**
   - **dotraining**
     Executes hundreds of agents, running hundreds of advanced algorithms and completes in minutes.  A master agent then chooses the BEST algorithm that best  models your data.
   - **dopredictions**
     After training, make high quality predictions - takes 1-2 seconds.
   - **hyperpredictions**
     After training, make high quality predictions - takes less than half a second (about ~100 milliseconds). Users can also generate predictions using **non-python code** such as JAVA.  Using the **maadshyperpredictions.CLASS** file, java apps can call the MAADS prediction server to return predictions very fast.  Other apps, using **any** other language, can also call the MAADS prediction server using standard TCP/IP client/server communication protocols:  This gives MAADS users' the maximum flexibility to integrate MAADS predictions in any solution!
	 
**Support functions:**

- **dolistkeys**
        - List all of the keys associated with the data you have analysed. 
- **dolistkeyswithkey**
        - List data associated with a single key.
- **dodeletewithkey**
        - Permanently delete all data associated with your key.
- **returndata**
        - Returns data from the string buffer.
- **getpicklezip**
        - Automatically downloads a ZIP file containing the optimal algorithms.  Users can modify the parameter estimates as they wish.
- **sendpicklezip**
        - Automatically upload a ZIP file containing the optimal algorithms to MAADS. The optimal algorithms will immediately take effect for predictions.
- **deploytoprod**
        - Automatically deploy the optimal algorithms to another MAADS server (i.e. production); MAADS will read the ZIP file, extract the algorithms and make all database updates.  This function is useful when your MAADS training server(s) and MAADS prediction server(s) are separate.  A powerful way to integrate MAADS in a distributed architecture is to automatically train your data, then deploy the optimal algorithms to some other server for predictions.  This is a great way to scale your analytics in a large (global) entreprise setting, seamlessly and fast, with MAADS!
		
**Natural Language Processing (NLP):**

- **nlp**
   - Automatically perform NLP to summarize large amounts of text data.  Specifically, there are three data sources one can use:
       - **Website URL:** you can pass a URL to the NLP function and it will automatically scrape the site and return a summary of the text.
       - **PDF:** Send a PDF to be summarized.
       - **Text:** Paste text to be summarized.
       - This allows users to integrate NLP in unique and powerful ways with advanced analytics.

**First import the Python library.**

**import maads**

1. **maads.dotraining(CSV_local_file, username, password, feature_analysis, remove_outliers, has_seasonality, dependent_variable, your_company_name, your_email,maadsurl,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy)**

**Parameters:**	

*CSV_local_file* : string, required

- A local comma-separated-file (csv) with Date in the first column.  Date must be MM/DD/YYYY format.  
- All other data must be numbers.

*username* : string, required
     
- A username issued by the system administrator. 

*password* : string, required 

- A password issued by the system administrator.

*feature_analysis* : int, required, 1 or 0

- If 1, then a feature analysis will be done on your data along with training.  If 0, no analysis is done. If -1, features will be generated, and downloaded to your local computer folder WITHOUT training.
    
*remove_outliers* : int, required, 1 or 0

- If 1, then outliers will be removed from your data.  If 0, no outliers are removed.

*has_seasonality* : int, required, 1 or 0
      
- If 1, then your data will be modeled for seasonality: Winter, Summer, Shoulder. If 0, then your data will 
  not be modeled for seasonality.  If modeling for seasonality, ensure you have enough data points that 
  covers the seasons, usually 1 year of data.

*dependent_variable* : string, required
       
- This is the dependent variable in your file.  All other variables will be modeled as independent variables.
       
*your_company_name* : string, required

- Indicate your company name, the one associated with your username. 
       
*your_email* : string, required       
        
- Indicate your email, the one associated with your username. 

*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and password. 
	   
*summer* : string, optional

- Indicate summer months.  The default value is '6,7,8' for North America.  If you are analysing other continents you could change this value. 

*winter* : string, optional

- Indicate winter months.  The default value is '12,1,2,3' for North America.  If you are analysing other continents you could change this value. 

*shoulder* : string, optional

- Indicate shoulder months.  The default value is '4,5,9,10,11' for North America.  If you are analysing other continents you could change this value. 

*trainingpercentage* : number between 40 and 80, optional

- Indicates how much of the complete data set to you as the Training data set. The default value is 75% or 75, the rest is used for test or validation.

*retrainingdays* : number, optional

- Indicates how many days to wait, from initial training, to re-train the model. This is convenient to automate re-training of models to take advantage of new data.  Default value is 0, for no re-training.

*retraindeploy* : number, 0 or 1, optional

- Indicates whether to deploy (retraindeploy=1) the optimal algorithm to a server (i.e. production) for immediate use after re-training. This assumes FTP server is listed in the MAADS lookup table. Default value is 0, for no deployment after re-training.

**Returns:** string buffer, PDF of Results, CSV of Prediction Data
        
- The string buffer contains the following sections:
        
- DATA: : This consists of the feature selection results
- PKEY: : This is the key to the BEST algorithm and must be used when making predictions.

			

**2. maads.dopredictions(attr,pkey,inputs,username,password,your_company_name, your_email,maadsurl)**

**Parameters:**	

*attr* : int, required

- This value should be 0.  It may change to other values in the future.

*pkey* : string, required

- This value must be retrieved from dotraining.  Note you can store PKEY after you have trained your file. 
  Training does not have to run before predictions, as training occurs more infrequently.

*inputs* : string, required
     
- This is a row of input data that must match the independent variables in your CSV. For example, if your 
  trained file is: Date, A, B, C, D and A is your dependent variable, then your inputs must be:
  Date, B, C, D

*username* : string, required
     
- A username issued by the system administrator. 

*password* : string, required 

- A password issued by the system administrator.
     
*your_company_name* : string, required

- Indicate your company name, the one associated with your username. 
       
*your_email* : string, required       
        
- Indicate your email, the one associated with your username. 
     
*maadsurl* : string, required
      
- Indicate location of MAADS server.  You would have received this URL when you received your username and password. 
	 
**Returns:** string buffer
        
- The string buffer contains the following sections:
        
  DATA: : This contains your prediction.

**3. maads.hyperpredictions(host,port,username,password,company,email,pkey,inputdata)**

**Parameters:**	

*host* : string, required

- The host is the webserver that connects to the MAADS prediction server.  This will be provided by the MAADS administrator.

*port* : int, required

- This is the port that the MAADS prediction server listens on.  This will be provided by the MAADS administrator.

*username* : string, required
     
- A username issued by the system administrator. 

*password* : string, required 

- A password issued by the system administrator.
     
*your_company_name* : string, required

- Indicate your company name, the one associated with your username. 
       
*your_email* : string, required       
        
- Indicate your email, the one associated with your username. 
     
*pkey* : string, required
      
- This is the key to the optimal algorithm.

*inputdata* : string, required
      
- This is the input data for the optimal algorithm to produce a prediction.
	 
**Returns:** Number, prediction value
        
- The difference between doprediction and hyperpredictions is that do prediction returns 
        predictions in a few seconds, hyperpredictions returns predictions in milliseconds.  So if you require very fast predictions
		use hyperpredictions.  
  
**4. maads.returndata(thepredictions, section_attr)**

**Parameters:**	

*thepredictions* : string buffer

- This value is returned from dopredictions.

*section_attr* : string buffer

This value can be any one of the values:
        
- PKEY: : This returns the key from the dotraining function.  Note the semi-colon.
- DATA: : This returns the data from the dotraining or dopredictions functions.  Note the semi-colon.
- ALGO0: : This returns the BEST algorithm determined by MAADS - without seasonality.
- ACCURACY0: : This returns the forecast accuracy for the BEST algorithm - without seasonaility.
- SEASON0: : This returns allseason - for no seasonality.
- ALGO1: : This returns the BEST algorithm determined by MAADS for WINTER.
- ACCURACY1: : This returns the forecast accuracy for the BEST algorithm for WINTER.
- SEASON1: : This returns WINTER.
- ALGO2: : This returns the BEST algorithm determined by MAADS for SUMMER.
- ACCURACY2: : This returns the forecast accuracy for the BEST algorithm for SUMMER.
- SEASON2: : This returns SUMMER.
- ALGO3: : This returns the BEST algorithm determined by MAADS for SHOULDER season.
- ACCURACY3: : This returns the forecast accuracy for the BEST algorithm for SHOULDER season.
- SEASON3: : This returns SHOULDER.
        
**Returns:** string buffer
        
- The string buffer contains the prediction or the key or the feature analysis.
        
**5. maads.dodeletewithkey(username,password,company,email,pkey,maadsurl)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*pkey* : string buffer

- The key you want deleted.  This can be attained from dolistkeys function.

*maadsurl* : string, required
     
- Indicate location of MAADS server.  You would have received this URL when you received your username and password. 
	 
**Returns:** NULL
        
- Deletes all files and tables associated with the key permanently.
        
**6. maads.dolistkeys(username,password,company,email,maadsurl)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and password. 
	 
**Returns:** string buffer
        
- Lists all the keys associated with your username.
        
**7. maads.dolistkeyswithkey(username,password,company,email, pkey,maadsurl)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*pkey* : string buffer

- The key you want returned.

*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and password. 
	 
**Returns:** string buffer
        
- Returns the information (with independent variables) associated with your key.

        
**8. maads.getpicklezip(username,password,company,email, pkey,url,localfolder)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS server.  This is the root location of the MAADS folder in the webserver. 

*localfolder* : string, required
       
- Indicates local folder location where file will be saved (i.e. C:/MAADS). Please use folder slashes.
	 
**Returns:** ZIP File
        
- This is a binary ZIP file and stored in the location of the localfolder.
        
**9. maads.sendpicklezip(username,password,company,email, pkey,url,localfilename)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*localfilename* : string, required
       
- Indicates local filename to be sent to the server. The file name should have a proper file format: key_DEPLOYTOPROD.zip 
	   
**Returns:** Server Response.
        
- The ZIP file will be stored and read by MAADS and all necessary changes will immediately take effect.
        
**10. maads.deploytoprod(username,password,company,email, pkey,url,localfilename,ftpserver,ftpuser,ftppass)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*localfilename* : string, optional
       
- Indicates local filename to be sent to the server. If indicating localfilename it must have a proper file format: key_DEPLOYTOPROD.zip 

*ftpserver* : string, optional
       
- Indicates ftp server you want to deploy the optimal algorithms to for predictions. If no FTP server is specified a default FTP server
  will used as listed on the MAADS server.  If none is listed this function will fail.
	   
*ftpuser* : string, optional
       
- Indicates ftp username to login to ftp server. If no FTP username is specified a default FTP username
  will used as listed on the MAADS server.

*ftppass* : string, optional
       
- Indicates ftp password to login to ftp server.  If no FTP password is specified a default FTP password
  will used as listed on the MAADS server.
	   
**Returns:** Server Response.
        
- The ZIP file will be stored and deployed to the MAADS PROD server (with FTP connection) and read by MAADS and all necessary changes will immediately take effect. The functions: dopredictions and hyperpredictions can immediately be used.

**11. maads.nlp(username,password,company,email, buffer,url,detaillevel)**

**Parameters:**	

*username* : string buffer

- The username given to you by system administrator.

*password* : string buffer

- The password given to you by system administrator.

*company* : string buffer

- Your company assicated with your username.

*email* : string buffer

- Your email associated with your username.

*buffer* : string buffer

- The data source to be summarized: URL, PDF, TEXT

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*detaillevel* : int, optional
       
- Indicates how detailed you want the summary to be.  This value ranges from 10-100, the lower the number the more detailed the summary will be.  The default is 30. 
	   
**Returns:** Server Response.
        
- The summary of the text.
			
**Simple Example**      

#############################################################

Author: Sebastian Maurice, PhD

Copyright by Sebastian Maurice 2018

All rights reserved.

Email: Sebastian.maurice@gmail.com

#############################################################


** IMPORT THE MAAADS LIBRARY*
 import maads

** IMPORT ADDITIONAL LIBRARY**
 import imp


** LOAD ANY DATABASE LIBRARY TO STORE PREDICTIONS**
 sqlconn = imp.load_source('sqlconn','C:\\sqlsrvconnpython.py')

** OPEN DATABASE CONNECTION**
 connection = sqlconn.doconnect()

 cur = connection.cursor()

** TEST DATA    **   
 inputs = '1/12/2018,37.76896'

 username='demouser'

 password='XXXXX'

 pkey='demouser_test2log_csv'

 company='otics'

 email='sebastian.maurice@gmail.com'

 url='http://www.otics.ml/stocks/maads/remotemasstreamremote.php'


** DO TRAINING - SERVER RETURNS A KEY THAT POINTS TO THE BEST ALGORITHM**
 thedata=maads.dotraining('C:\\test2log.csv',username,password,1,0,0,'depvar','otics',email,url)

** PARSE RETURNED DATA**
 pkey=maads.returndata(thedata,'PKEY:')

 algo=maads.returndata(thedata,'ALGO0:')

 accuracy=maads.returndata(thedata,'ACCURACY0:')
      
** DO PREDICTIONS WITH THE RETURNED KEY**
 thepredictions=maads.dopredictions(0,pkey,inputs,username,'XXXXXX',company,email,url)

** PARSE THE DATA**
 prediction=maads.returndata(thepredictions,'DATA:')


** INSERT PREDICTIONS TO ANY DATABASE TABLE**
 forecastdate=inputs.split(',')[0]

 predictionvalue=prediction[2]

 accuracy=prediction[3]

 SQL="INSERT INTO PREDICTIONS VALUES('%s','%s','%s','%s','%s',%.3f,%.3f)" % (forecastdate,username,pkey,company,inputs,predictionvalue,accuracy)

 cur.execute(SQL)

 cur.commit()

** CLOSE THE DATABASE CONNECTION**
 cur.close()

        
