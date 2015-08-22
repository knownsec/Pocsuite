----
cmd2
----

:Author: Catherine Devlin, http://catherinedevlin.blogspot.com

`cmd2` is a tool for writing command-line interactive applications.  It is based on the Python Standard Library's `cmd` module, and can be used anyplace `cmd` is used simply by importing `cmd2` instead.

`cmd2` provides the following features, in addition to those already existing in `cmd`:

- Searchable command history
- Load commands from file, save to file, edit commands in file
- Multi-line commands
- Case-insensitive commands
- Special-character shortcut commands (beyond cmd's `@` and `!`)
- Settable environment parameters
- Parsing commands with flags
- Redirection to file with `>`, `>>`; input from file with `<`
- Bare '>', '>>' with no filename send output to paste buffer
- Pipe output to shell commands with `|`
- Simple transcript-based application testing

Instructions for implementing each feature follow.

- Searchable command history

    All commands will automatically be tracked in the session's history, unless the command is listed in Cmd's excludeFromHistory attribute.  
    The history is accessed through the `history`, `list`, and `run` commands 
    (and their abbreviations: `hi`, `li`, `l`, `r`).
    If you wish to exclude some of your custom commands from the history, append their names
    to the list at Cmd.ExcludeFromHistory.

- Load commands from file, save to file, edit commands in file

    Type `help load`, `help save`, `help edit` for details.
  
- Multi-line commands

    Any command accepts multi-line input when its name is listed in `Cmd.multilineCommands`.
    The program will keep expecting input until a line ends with any of the characters 
    in `Cmd.terminators` .  The default terminators are `;` and `/n` (empty newline).
    
- Case-insensitive commands

    All commands are case-insensitive, unless `Cmd.caseInsensitive` is set to `False`.
  
- Special-character shortcut commands (beyond cmd's "@" and "!")

    To create a single-character shortcut for a command, update `Cmd.shortcuts`.
  
- Settable environment parameters

    To allow a user to change an environment parameter during program execution, 
    append the parameter's name to `Cmd.settable`.
    
- Parsing commands with `optparse` options (flags) 

    ::
    
        @options([make_option('-m', '--myoption', action="store_true", help="all about my option")])
        def do_myfunc(self, arg, opts):
            if opts.myoption:
                ...
            
    See Python standard library's `optparse` documentation: http://docs.python.org/lib/optparse-defining-options.html
    
cmd2 can be installed with `easy_install cmd2`

Cheese Shop page: http://pypi.python.org/pypi/cmd2

Example cmd2 application (example/example.py) ::

    '''A sample application for cmd2.'''
    
    from cmd2 import Cmd, make_option, options, Cmd2TestCase
    import unittest, optparse, sys
    
    class CmdLineApp(Cmd):
        multilineCommands = ['orate']
        Cmd.shortcuts.update({'&': 'speak'})
        maxrepeats = 3
        Cmd.settable.append('maxrepeats')
    
        @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
                  make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
                  make_option('-r', '--repeat', type="int", help="output [n] times")
                 ])
        def do_speak(self, arg, opts=None):
            """Repeats what you tell me to."""
            arg = ''.join(arg)
            if opts.piglatin:
                arg = '%s%say' % (arg[1:], arg[0])
            if opts.shout:
                arg = arg.upper()
            repetitions = opts.repeat or 1
            for i in range(min(repetitions, self.maxrepeats)):
                self.stdout.write(arg)
                self.stdout.write('\n')
                # self.stdout.write is better than "print", because Cmd can be
                # initialized with a non-standard output destination
    
        do_say = do_speak     # now "say" is a synonym for "speak"
        do_orate = do_speak   # another synonym, but this one takes multi-line input
    
    class TestMyAppCase(Cmd2TestCase):
        CmdApp = CmdLineApp
        transcriptFileName = 'exampleSession.txt'
    
    parser = optparse.OptionParser()
    parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
    (callopts, callargs) = parser.parse_args()
    if callopts.unittests:
        sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
        unittest.main()
    else:
        app = CmdLineApp()
        app.cmdloop()

The following is a sample session running example.py.
Thanks to `TestMyAppCase(Cmd2TestCase)`, it also serves as a test 
suite for example.py when saved as `exampleSession.txt`.  
Running `python example.py -t` will run all the commands in the
transcript against `example.py`, verifying that the output produced
matches the transcript.

example/exampleSession.txt::

    (Cmd) help
    
    Documented commands (type help <topic>):
    ========================================
    _load  edit  history  li    load   pause  run   say  shell      show 
    ed     hi    l        list  orate  r      save  set  shortcuts  speak
    
    Undocumented commands:
    ======================
    EOF  cmdenvironment  eof  exit  help  q  quit

    (Cmd) help say
    Repeats what you tell me to.
    Usage: speak [options] arg
    
    Options:
      -h, --help            show this help message and exit
      -p, --piglatin        atinLay
      -s, --shout           N00B EMULATION MODE
      -r REPEAT, --repeat=REPEAT
                            output [n] times
    
    (Cmd) say goodnight, Gracie
    goodnight, Gracie
    (Cmd) say -ps --repeat=5 goodnight, Gracie
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    (Cmd) set
    prompt: (Cmd)
    editor: gedit
    echo: False
    maxrepeats: 3
    (Cmd) set maxrepeats 5
    maxrepeats - was: 3
    now: 5
    (Cmd) say -ps --repeat=5 goodnight, Gracie
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    (Cmd) hi
    -------------------------[1]
    help
    -------------------------[2]
    help say
    -------------------------[3]
    say goodnight, Gracie
    -------------------------[4]
    say -ps --repeat=5 goodnight, Gracie
    -------------------------[5]
    set
    -------------------------[6]
    set maxrepeats 5
    -------------------------[7]
    say -ps --repeat=5 goodnight, Gracie
    (Cmd) run 4
    say -ps --repeat=5 goodnight, Gracie
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    OODNIGHT, GRACIEGAY
    (Cmd) orate Four score and
    > seven releases ago
    > our BDFL
    > blah blah blah
    >
    >
    Four score and seven releases ago our BDFL blah blah blah
    (Cmd) & look, a shortcut!
    look, a shortcut!
    (Cmd) say put this in a file > myfile.txt
    (Cmd) say < myfile.txt
    put this in a file
    (Cmd) set prompt "---> "
    prompt - was: (Cmd)
    now: --->
    ---> say goodbye
    goodbye