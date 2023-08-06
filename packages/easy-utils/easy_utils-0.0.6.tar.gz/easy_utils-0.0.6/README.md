Functions I've used accross multiple projects, more info in this README to come

    #alert(alarm, x) counts down from x and prints int x and a string alarm to console

    alert('Till countdown', 10)

    #check_dir(child, parent) looks for a child directory in a parent directly, if there is no child dir then one is created 
    
    check_dir('log', '~')

    #check_file(fname, file_dest) ensures that a file is not in a directory, if it is not in the directory then the a path is provided for file creation 
    
    check_file('somefile.txt', '~/projects')

    #log_it(text, dest_dir) takes in string text and a string file destination folderand creates a file named with timestamp
    
    log_it('this is a test', './log/')

    #run_in_background(args) takes in a string shell command and runs it as a background process
     run_in_background('firefox')

    #limit_proc(proc,limit) takes in a string process name and an int limit, limit represents a threshold of a certain process. If limit is reached then a simple spinlock activates and activly waits until the process count is no longer at the limit

    limit_proc('curl', 5)

    #kill_proc(proc) takes in a string process name and kills processes with that name

    kill_proc('curl')
