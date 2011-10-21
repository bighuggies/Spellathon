'''
Handle operations performed on the .config file for Spellathon. Very fragile
at the moment.

'''
def set_admin(user):
    '''Write a line to the config file to mark an account as administrative.
    
    Arguments:
    user -- The user to be marked as an admin.
    
    '''
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