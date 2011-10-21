'''
Created on 22/10/2011

@author: andrew
'''
def set_admin(user):
        cfg = open('.config', 'w')
        cfg.write('admin=' + user.username)
        cfg.close

def get_admin():
    '''Load the configuration file.
    
    Returns:
    The name of the administrator account.
    
    '''
    try:
        cfg = open('.config', 'r')
        admin = cfg.readline().split('=')
        cfg.close()
        if admin[0] == 'admin':
            return admin[1]
        else:
            return None
    except IOError:
        return None    