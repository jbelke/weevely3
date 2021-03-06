Weevely3 
=======

> Weevely3 is a complete rewrite of [Weevely](https://github.com/epinna/Weevely), the web shell for penetration testing included in [Kali](http://www.kali.org/) and [BackBox](http://www.kali.org/) Linux


> This project is still at version 3.0beta and a lot of features are currently missing.


> If you are a developer or a curious user and desire to contribute, you can to start reading the tutorial [Developing a new module ](https://github.com/epinna/weevely3/wiki/developing-a-new-module) and the [TODO list](https://github.com/epinna/weevely3/issues/1).

Weevely is a PHP web shell that provides a weaponized telnet-like interface to administrate a remote web access.

It is a swiss army knife to administrate a web account, even in restricted remote environments. Weevely is an essential tool for web application post exploitation, access maintaining, target security audit, pivot deeper in the target network, and much more. 

### The modular framework

Weevely modules extend the terminal providing a layer to interact to the remote target. 

The modules feature:

* Shell/PHP telnet-like network terminal
* Common server misconfigurations auditing
* SQL console pivoting on target network 
* HTTP traffic proxy through target
* Mount target file system to local mount point
* Run scans or pivoted exploiting through target network
* File transfer from and to target
* Spawn reverse and direct TCP shells
* Bruteforce SQL accounts through target system users

### The backdoor agent

The remote agent is a very low footprint agent that receives the dynamically injected code from the client, extending the client functionalities over the network at run-time. The agent code is polymorphic and hardly detectable by AV and HIDS. The communication is covered and obfuscated within the HTTP protocol using steganographic techniques.

### Modules development

Weevely also provides python API which can be used to develop your own module to implement internal audit, account enumerator, sensitive data scraper, network scanner, make the modules work as a HTTP or SQL client and do a whole lot of other cool stuff.

> If you are a developer or a curious user and desire to contribute, you can to start reading the tutorial [Developing a new module ](https://github.com/epinna/weevely3/wiki/developing-a-new-module) and the [TODO list](https://github.com/epinna/weevely3/issues/1).
