# Setting up your environment to work with the LYNX API and Python

**Requirements**:

- [API Software](https://api.lynx.academy/API_versions) Installed
- TWS Running
- Socket Connection enabled and configured: *Configure->API->Settings* *(Port - 7496 & Enable ActiveX and Socket Clients)*
- Python 3.6 or higher



**Installation:**

> After the API software has been downloaded and installed, the folder should have the following contents:

![](informative_examples/request_market_data/images/tws_folder_content.png)

> In order to include the API library in the global site-packages you must navigate to *".../TWS_installation_folder/source/pythonclient"*:

![](informative_examples/request_market_data/images/tws_folder_content_setup.png)

> Finally, run the python script *setup.py* in a console with the following command - *python setup.py install* :

![](informative_examples/request_market_data/images/console_setup.png)
