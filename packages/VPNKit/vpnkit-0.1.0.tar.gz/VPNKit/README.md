**VPNKit**

VPNKit is an OpenVpn client application for connect to a remote server. Work of the application based on the OpenVpn service which allow to hide your traffic in a tun/tap interface.

For work with application you must have  account on VPNKit server. 

**Installation**

    $ sudo pip install VPNKIt

**Usage**

Enter 'vpnkit' in terminal. You can see this start menu:

    $ Choose operations[start(default)|new|settings|exit]: 

- "start" - default option.If you press enter application will be started with parameters that was saved in settings 
- "new" - enter parameters  and start new connection to the server
- "settings" - option for checking current application settings
- "exit" - close application

After start and up connection with server you can choose two options:

    $ Choose [close|new]: 

- "close" - close the application
- "new" - kill current connection and return to the start menu


**Change log**


[0.1.0] - 2018-12-18

  **Added**

First release on PyPI.
