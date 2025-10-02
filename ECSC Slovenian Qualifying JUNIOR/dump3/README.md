## Challenge Name: Dump3
Categories: Forensic
Difficulty: Medium

## Description: 
Please download and analyze a dump file from RESOURCES

## Solution

### Security Questions

    What OS was the machine running? (md5 of this response = 48a574e5ff37e73edf8aeb69fdd11fa0 or in lower case = e243201a81772b243703ba893a3da93b)
    How many processes were running in the machine? (result = int)
    What is the SHA-1 of /var/run/utx.active
    What user is logged in graphical desktop? (md5 of this response = 56a9e9bd413d2c62e5749f0d724a1d17
    What file was used as desktop background (full path)? (md5 of this response = 9df088501aeb1ad9404bc67119b1bc6a
    What flag was on the screen?

### Flag

The flag is the md5sum of the responses of questions 1-6. The flag has been calculated using the command below (responses separated with a : and converted to lowercase).

echo -n "response1:response2:response3:response4:response5:response6" | tr '[:upper:]' '[:lower:]' | md5sum 

### Hint

Flag; Only the md5 of the output (not the -)

## Solution

Didn't solve this challenge.


---
[Back to home](../README.md)
