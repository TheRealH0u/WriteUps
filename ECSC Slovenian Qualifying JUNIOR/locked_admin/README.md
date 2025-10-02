## Challenge Name: Locked Admin
Categories: Forensic, Penetration Testing
Difficulty: Medium

## Description: 
This time you must investigate a recent attack on a web server. Attackers have dropped some password-protected site there. Your friends from Incident Response Department managed to get a network capture file from one of the attackers' computers.

Please start the web service from `RESOURCES`. (Note: This started a web server with a website that just had a login page. Logging in = you get the flag)

Please download the following [capture.pcapng](capture.pcapng) file

## Solution

Analyzing the pcapng file, we can see that there are some UDP requests and some HTTP requests, but there's really no useful data in them (besides seeing that the attacker accessed the webpage we need to get into). The majority of the traffic is USB packets, and we can use the [ctf-usb-keyboard-parser](https://github.com/carlospolop-forks/ctf-usb-keyboard-parser) to get the keystrokes the attacker sent. We get the following string:

`icsadmin   0nc3O@g@in←⌫1→W3need←⌫⌫33@p@←⌫P→sswo⌫0$d!⌫_⌫`

We follow the keys the attacker pressed and get this:

`0nc3O@g@1nW3n33@P@ssw0$dd`

This password doesn't work though, so we rearrange it a bit to make it make more sense:

`Onc3@g@1nW3n33d@P@ssw0$d`

We use this password to log in and get the flag.

---
[Back to home](../README.md)
