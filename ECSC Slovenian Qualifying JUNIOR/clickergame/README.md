## Challenge Name: Clicker Game
Categories: Android
Difficulty: Medium

## Description: 
This challenge is about `Android APK` analysis. The flag is hidden in the `APK`. Can you find it?
APK

Get the apk [here](ClickerGame.apk)

Flag Format: `ctf{string}`

### Artifact Files:
* [ClickerGame.apk](ClickerGame.apk)

## Solution

We get an Android app that is basically a clicker game where you can 'buy' the flag for a large amount of money. The simplest way I thought of getting that flag is to use CheatEngine with an emulator and change the value of the money to a large number.

After doing that we click on "Buy" and get the flag.

---
[Back to home](../README.md)
