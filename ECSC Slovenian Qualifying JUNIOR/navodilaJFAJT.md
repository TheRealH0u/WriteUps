# [FORENSICS] Samuel Dupapi

## Opis naloge
Our field operations team has managed to seize the computer of Samuel Dupapi, a notorious black-hat hacker responsible for over $3 billion in damages. Forensic analysis of the data stored on the laptop has concluded that it is not of much use, but it has been noted that Dupapi used his computer to log into his command and control server website. Attached is a copy of his user directory (C:\Users\Samuel Dupapi) and the registry hives of his computer (C:\Windows\System32\config). Can you recover the password Dupapi used to log into the website?

P.S. Our insider information has revealed that Dupapi's Windows login password – not to be confused with the website password you're looking for – consisted of numbers only. Perhaps he is not the genius we thought he was.

## Predlagana težavnost
Srednja: korakov je kar nekaj, a je pri vsem mogoče najti rešitve z Googlom. Pri dešifriranju Chromovih gesel je sicer veliko zadetkov, ki so zastareli ali predvidevajo, da izvajamo online napad, a je mogoče z nekaj truda najti tudi delujoča navodila za offline napad.

## Zastavica
`ctf{P4ssw0rd_hyg13n3_1s_f0r_l0s3rS}`

## Postopek reševanja
Pri postopku so uporabljeni Linux (skupaj s shellom in programi `zip`, `base64`, `tail` in `jq`), Impacket CLI orodja (`impacket-secretsdump` in `impacket-dpapi`), in [CyberChef](https://toolbox.snopyta.org/). Vse je z malo več truda mogoče izvesti tudi na Windowsih.

### Pridobitev DPAPI ključa
1) Naložimo in razširimo `files.zip`:
```
$ unzip files.zip
/.../
```

2) Iz Windowsovega registra preberemo hashana gesla:
```
$ impacket-secretsdump -system 'Registry Hives/SYSTEM' -sam 'Registry Hives/SAM' LOCAL
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Target system bootKey: 0x5a9477bda9b57354367f2b04f0b89a1d
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:3ddfe6ba890eb8fd3fa3e9fa796364f4:::
Samuel Dupapi:1001:aad3b435b51404eeaad3b435b51404ee:efc541273700077bbaec6a4941776b2a:::
[*] Cleaning up...
```

3) Hash za uporabnika Samuel Dupapi shranimo v datoteko in ga scrackamo. Pri tem si pomagamo z dejstvom, da vsebuje geslo le števila.

Pri iskanju gesla začnemo z `?d?d?d?d?d?d?d`, saj Windows privzeto dolžino gesel omeji na najmanj 7 znakov, in nato dodajamo `?d`-je, dokler gesla ne najdemo.

Hashcat (za uporabnike s podprtimi GPUji):
```
/.../
$ hashcat -a 3 -m 1000 -O hash '?d?d?d?d?d?d?d?d'
/.../
$ hashcat -a 3 -m 1000 -O hash '?d?d?d?d?d?d?d?d?d'
/.../
$ hashcat -a 3 -m 1000 -O hash '?d?d?d?d?d?d?d?d?d?d'
hashcat (v6.2.6) starting
/.../
efc541273700077bbaec6a4941776b2a:5720133793
```

John the Ripper (za vse ostale):
```
/.../
$ john --format=NT hash -mask='?d?d?d?d?d?d?d?d'
/.../
$ john --format=NT hash -mask='?d?d?d?d?d?d?d?d?d'
/.../
$ john --format=NT hash -mask='?d?d?d?d?d?d?d?d?d?d'
Using default input encoding: UTF-8
Loaded 1 password hash (NT [MD4 256/256 AVX2 8x3])
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
/.../
5720133793       (Samuel Dupapi)
Use the "--show --format=NT" options to display all of the cracked passwords reliably
Session completed.
```

*Opomba: bruteforce je sicer zahtevan, a to ne bi smelo izključiti igralcev s slabšo strojno opremo. Moj poceni prenosnik iz 2016 doseže na JtR benchmarku 17.2 MH/s, torej bi bil čas da pokrije celotno iskano polje 7 do 10 številk okoli 11 minut:*

	Σ(10^x, 7, 10) / (17.2M/s) ≈ 10 min + 45.930s

*moj manj poceni prenosnik iz 2019 doseže na hashcat benchmarku 34629.7 MH/s, torej pokrije celotno iskano polje v manj kot sekundi, na JtR pa doseže 774.1 MH/s, torej potrebuje okoli 17s. Če želite, da geslo skrajšam oziroma uporabim kaj drugega, mi pišite.*

4) Z najdenim geslom dešifriramo DPAPI ključ. DPAPI ključi se nahajajo v `~\AppData\Roaming\Microsoft\Protect`, v našem primeru obstaja le eden:
```
$ impacket-dpapi masterkey -password '5720133793' -file 'Samuel Dupapi/AppData/Roaming/Microsoft/Protect/S-1-5-21-860164213-2925291848-1991998619-1001/fbca7af1-fed2-4031-8883-beb1f517d321' -sid 'S-1-5-21-860164213-2925291848-1991998619-1001'
Impacket v0.11.0 - Copyright 2023 Fortra

[MASTERKEYFILE]
Version     :        2 (2)
Guid        : fbca7af1-fed2-4031-8883-beb1f517d321
Flags       :        5 (5)
Policy      :        0 (0)
MasterKeyLen: 000000b0 (176)
BackupKeyLen: 00000090 (144)
CredHistLen : 00000014 (20)
DomainKeyLen: 00000000 (0)

Decrypted key with User Key (SHA1)
Decrypted key: 0x523f60d20253b5786a73008bc1c924f93da3770f2fbdb37cb5d42d849559620e275d03949d63a2a21868f6b82dbdc6a2fc1921f5936dfb77802a860ca624034c
```

*Opomba: korake za pridobitev uporabnikovega gesla je mogoče preskočiti in neposredno crackati DPAPI ključ, a je crackanje le-tega več magnitud počasnejše (s hashcatom dosežem pičlih 21534 H/s). Preprečitev tega je bil tudi razlog, da nisem izbral gesla iz wordlista.*

### Dešifriranje Chromiumovih shranjenih gesel
1) Pridobimo Chromiumov glavni ključ, s katerim so zašifrirana gesla spletnih strani. Prvih pet bajtov preskočimo, saj niso del zašifriranega ključa:
```
$ cat 'Samuel Dupapi/AppData/Local/Chromium/User Data/Local State' | jq -r '.os_crypt.encrypted_key' | base64 -d | tail -c +6 > chromium-master-key
```

2) Chromiumov glavni ključ dešifriramo z uporabo prej pridobljenega DPAPI ključa:
```
$ impacket-dpapi unprotect -k 0x523f60d20253b5786a73008bc1c924f93da3770f2fbdb37cb5d42d849559620e275d03949d63a2a21868f6b82dbdc6a2fc1921f5936dfb77802a860ca624034c -file chromium-master-key
Impacket v0.11.0 - Copyright 2023 Fortra

Successfully decrypted data
 0000   59 56 C3 05 E8 AD 8B BD  2F A1 CF 2B B4 D6 82 9E   YV....../..+....
 0010   4F CF FC DD 8E 9F 2C 32  51 F9 BD 26 87 84 3A 62   O.....,2Q..&..:b
```

3) Pridobimo zašifrirano geslo spletne strani. Le-tega je potrebno razbiti na tri dele: prve tri bajte preskočimo, naslednjih 12 bajtov uporabimo kot IV, zadnjih 16 bajtov uporabimo kot GCM tag, vmesne bajte pa uporabimo kot ciphertext:
```
$ sqlite3 'Samuel Dupapi/AppData/Local/Chromium/User Data/Default/Login Data' 'SELECT hex(password_value) FROM logins;'
763130|194086b532feb1544c8b89e0|0153fde59fdd964bce6fb4942535c0b63f001b01131073a68c21c832810256890305bd|673adff67725276ff816d7cf42a1b4a2
```

```
763130|194086b532feb1544c8b89e0|0153fde59fdd964bce6fb4942535c0b63f001b01131073a68c21c832810256890305bd|673adff67725276ff816d7cf42a1b4a2
       IV                       ciphertext                                                             tag
```

4) Vse podatke vstavimo v AES-GCM, da pridobimo zastavico: [CyberChef recept](https://toolbox.snopyta.org/#recipe=AES_Decrypt(%7B'option':'Hex','string':'5956c305e8ad8bbd2fa1cf2bb4d6829e4fcffcdd8e9f2c3251f9bd2687843a62'%7D,%7B'option':'Hex','string':'194086b532feb1544c8b89e0'%7D,'GCM','Hex','Raw',%7B'option':'Hex','string':'673ADFF67725276FF816D7CF42A1B4A2'%7D,%7B'option':'Hex','string':''%7D)&input=MDE1M2ZkZTU5ZmRkOTY0YmNlNmZiNDk0MjUzNWMwYjYzZjAwMWIwMTEzMTA3M2E2OGMyMWM4MzI4MTAyNTY4OTAzMDViZA)