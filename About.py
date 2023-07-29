version = 'V.2.1.0.3'
about = '''
    #    Talon framework, a single table data synchronization framework.
    # can be used in the final course design of college students, 
    # through the configuration of \033[1;33;4m'properties/service.xml'\033[0m File
    # to help users synchronize CRUD operations of a single table in the database.
    # Whether the server is alive or not, the crud operation data is always consistent. 
    # The built-in command parser about Talon command operation is built-in. 
    # By inputting 'help' to get the command rules 
    # for add,delete,update and view the command line

        \033[1;33;4m 1) The first field configured will be the PRIMARY KRY\033[0m
        \033[1;33;4m 2) to ensurerance the charcter of data tables is utf8\033[0m
        \033[1;33;4m 3) Ensure that the data type is varchar\033[0m
        \033[1;33;4m 4) Environment requirements: python3.7 or above, java1.8 or above\033[0m
            
            You just need to configure \033[1;33;4m'properties/service.xml'\033[0m correctly
        The rest of the work is left to TaLon
     ----------------------------------------------------
'''

help = '''

    \033[1;33;4mls-key PRIMARY KRY\033[0m "Search by primary key"
    
    \033[1;33;4mls attribute ...\033[0m "<attribute>:View a property of the entity "
       
        [no attribute] "show information for all entity sets"
    
    \033[1;33;4mdel attribute=value ...\033[0m "Deletes an entity that satisfies an attribute as Value"
    
    \033[1;33;4madd attribute=value attribute=value attribute=value...\033[0m "Add an entity and optionally assign an initial value to the attribute"
    
    \033[1;33;4mupdate PRIMARY KRY\033[0m " to Modify the entity"
    
    \033[1;33;4msum KEYS ,the 'KEYS' must be a computable data type\033[0m 
           
    \033[1;33;4mexit \033[0m    "sign out"           
'''

logo = '''
-WELCOME TO USE

  ▉ ▉ ▉ ▉ ▉ ▉         ▉           ▉               ▉ ▉ ▉          ▉         ▉
         ▉               ▉ ▉         ▉              ▉        ▉       ▉ ▉       ▉ 
         ▉              ▉   ▉        ▉             ▉          ▉      ▉  ▉      ▉
         ▉             ▉     ▉       ▉             ▉          ▉      ▉    ▉    ▉
         ▉            ▉ ▉ ▉ ▉      ▉             ▉          ▉      ▉      ▉  ▉
         ▉           ▉        ▉      ▉              ▉        ▉       ▉        ▉▉
         ▉          ▉          ▉     ▉ ▉ ▉ ▉ ▉     ▉ ▉ ▉         ▉         ▉
             
                                -iuput "help" can display the command
    '''


def print_fozu():
    print("                            _ooOoo_                     ")
    print("                           o8888888o                    ")
    print("                           88  .  88                    ")
    print("                           (| -_- |)                    ")
    print("                            O\\ = /O                    ")
    print("                        ____/`---'\\____                ")
    print("                      .   ' \\| |// `.                  ")
    print("                       / \\||| : |||// \\               ")
    print("                     / _||||| -:- |||||- \\             ")
    print("                       | | \\\\\\ - /// | |             ")
    print("                     | \\_| ''\\---/'' | |              ")
    print("                      \\ .-\\__ `-` ___/-. /            ")
    print("                   ___`. .' /--.--\\ `. . __            ")
    print("                ."" '< `.___\\_<|>_/___.' >'"".         ")
    print("               | | : `- \\`.;`\\ _ /`;.`/ - ` : | |     ")
    print("                 \\ \\ `-. \\_ __\\ /__ _/ .-` / /      ")
    print("         ======`-.____`-.___\\_____/___.-`____.-'====== ")
    print("                            `=---='  ")
    print("                                                        ")
    print("         .............................................  ")
    return 0