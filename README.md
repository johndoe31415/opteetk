# opteetk
opteetk is a set of small scripts and tooling to aid debugging of
[OP-TEE](https://github.com/OP-TEE/optee_os), a popular open source trusted
execution environment. I am not officially affiliated with the project.


## Examples
You can build and run a QEMU instance quickly by calling `run-optee`. Note that the
OP-TEE build scripts by default (`make run`) automatically create terminal instances
for the normal and secure world. If you want to reuse those without having to start
your own, it is easiest to first start a "default" run:

```
$ ./run-optee --internal-run-cmd build_environ.json
```

which will also fork the terminals. Then, subsequently, you can reuse those
terminals and restart `run-optee` with custom commands, e.g., with an attached
gdb debugger:

```
$ ./run-optee --attach-gdb --no-rebuild build_environ.json
```

This will then open up a third console, which has gdb already attached to the
target. The OP-TEE ELF symbols should also be already loaded in there. Note
that the CPU is initially halted. You can `c` (continue) in the debugger to let
the CPU run:

```
warning: No executable has been specified and target does not support
determining executable automatically.  Try using the "file" command.
0x00000000 in ?? ()
(gdb) c
Continuing.
```

This allows you to continue a basic setup first (e.g., doing initialization of
TLS handshakes with relatively good performance, no tracing at this point). At
some point, if you wish to commence tracing, you can simply Ctrl-C the debugger
to give it more instructions:

```
^C
Thread 1 received signal SIGINT, Interrupt.
0x801179c8 in ?? ()
```

Then, you can load the pagefault tracer module, which is Python code included
in this repository:

```
(gdb) source pagefault_tracer.py 
OP-TEE trace commands enabled.
```

This makes new commands available. Most interesting is `optee-pgtbl-autodump`,
which registers breakpoints and automatically dumps relevant information into
text files located in `/tmp`. These trace files can then later on be evaluated.

```
(gdb) optee-pgtbl-autodump 
Breakpoint 1 at 0xe10b2c8: file core/mm/fobj.c, line 105.
Breakpoint 2 at 0xe10b230: file core/mm/fobj.c, line 84.
Function "rrp_load_page" not defined.
Breakpoint 3 (rrp_load_page) pending.
```

Then, simply continue execution of code:

```
(gdb) c
Continuing.
```

## License
GNU GPL-3.
