# Scripted

There are many libraries for argument parsing and command line tools;
this is mine.




## Example

1. Define a controller class 
    
    ```python
    from scripted import Script


    script = Script()
    
    
    @script.add_controller
    @script.option('-a', '--option-a', dest='option_a', help='help text')
    @script.option('-b', '--option-b', dest='option_b', help='help text')
    class CommandController(script.Controller):
        """Main parser's help menu created from Controller class docstring.
    
        This is an example controller class used to make complex, deeply
        nested command line tools simple.
        """
    
        @script.argument('-c', '--c3', dest='a3', help='help text')
        @script.argument('c2', dest='c2', help='help text')
        @script.argument('c1', dest='c1', help='help text')
        def command_one(self):
            """Subparser help and desc created from command_one docstring."""
            self.fn.print(f"Called {self.fn.scope} with {self.args}")
            public = self.fn.prompt('username:', mode='stdin')
            private = self.fn.prompt('password:', mode='password')
            self.fn.print(public, private)
    
    
        @script.argument('-d', '--d3', dest='a3', help='help text')
        @script.argument('d2', dest='d2', help='help text')
        @script.argument('d1', dest='d1', help='help text')
        def command_two(self):
            """Sub-parser help menu created from command_two docstring."""
            self.fn.print(f"Called {self.fn.scope} with {self.args}")
    
    
        @script.argument('-e', '--e3', dest='a3', help='help text')
        @script.argument('e2', dest='e2', help='help text')
        @script.argument('e1', dest='e1', help='help text')
        def command_three(self):
            """Subparser help menu created from command_three docstring."""
            self.fn.print(f"Called {self.fn.scope} with {self.args}")
    
    
        def helper(self):
            """Undecorated methods are not introspected."""
            self.fn.print('Helper method')
    
    
    if __name__ == '__main__':
        script.execute()
    ```

2. Call the script however python scripts are called.

    ```bash
    python myapp.py -h
    python myapp.py command_one -h    
    ```
 