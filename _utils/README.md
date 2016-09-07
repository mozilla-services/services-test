Jenkins Infrastructure Utilities
--------------

* Files in this directory are used for infrastructure maintenance
* Use the env_vars.properties file to declare environment variables 
* In Jenkins job create an "Inject Environment Variables" section.  
Set: Properties File Path to: ${WORKSPACE}/env_vars.properties 
