import logging

#=========deprecated===========
#User Settings - Change These
email = "email@domain.com"
api_key = 'PUT API KEY HERE'
#===============================

#Advanced Settings
log = False #whether or not to log respective to below level
log_level = logging.INFO # Critical, Error, Warning, Info, Debug, Notset
network_proxies = {}
verify = True #True/False (Strongly advice against setting this to False) or path to CA_BUNDLE file or directory.
#Note from requests library: If directory, it must be processed using the c_rehas utility supplied with OpenSSL

#Don't need to change these 
client_id = 'OpenLab'
OPENLAB_URL= 'https://openlab.iris.no'
#OPENLAB_URL= 'https://dev.openlab.iris.no'
#OPENLAB_URL= 'https://build.openlab.iris.no'
#OPENLAB_URL= 'http://localhost:8888'

#NOTE when changing any of the above after installation, an uninstall/reinstall might be necessary
