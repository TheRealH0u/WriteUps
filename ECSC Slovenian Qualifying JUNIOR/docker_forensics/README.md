## Challenge Name: Docker Forensics
Categories: Forensic
Difficulty: Easy

## Description: 

Developers have noticed that latest version of a SSH jump host which they are using for remote access is acting weirdly. When inspecting logs, they notice logins from strange accounts that should not be there. Their own dev account password also seems to be compromised, as logins are coming from unknown IP addresses. Sysadmins have recreated the jump host container from the latest image but with no luck. Same activity is still seen. Could the Docker repository be hacked? Could the hackers have tampered with the image? You must find out!
Resources

Please pull the image from Docker Hub: `docker pull hackinglab/jumphost`

Flag Format: `UUID`

## Solution

I used the Dive ([Found here](https://github.com/wagoodman/dive)) tool to explore the container and found that a file is deleted in a certain layer. I then found that layer in `/var/lib/docker/overlay2` and found the flag hidden in the deleted file inside the layer.


---
[Back to home](../README.md)
