## Challenge Name: Encoded File Challenge
Categories: Fun
Difficulty: Easy

## Description: 
Download the encoded file [here](encoded). Decode it and find the flag.

Flag Format: `UUID`

## Solution

The file is a `.txt` file, but it's really an archive. I used 7zip to extract a `CSV`file from it.

The csv file looks like this:
```
3,20,42454143504d446255614571654a4a714442715a
21,20,66624f4c4f77382b664c77474d4f4c574666306d
4,20,4d4a4e4969556e6f674431436a526b4452706b61
13,20,617a647037654f2b7155345774614a6254695a4d
11,20,4a4d6774694b4a59583473704f51454e574a5762
9,20,6c5936766265643532683353494b61564e765970
17,20,734649546367464d335330556977764c765a4d53
14,20,656d5830376754744469475138464b5538517850
10,20,74383076444f5442484c656657746d364c685a44
25,20,3169564756505569546467716d4a49526e334b2b
5,20,4354554b616a514161507344714379494d51474d
1,20,516c706f4f54464257535a5457574e5a33554141
27,20,35536f663858636b5534554a426a57643141413d
24,20,6e746d70697056595772634b4c52757952544531
15,20,65585a4479455250567456456f4e447a7a4a562f
22,20,6574743131335245646f4c44356346464f787255
26,20,334d532f574737524f4e4766455a4f6f536e7861
16,20,736f53433644347262364d4c6f64317551784d77
19,20,7641764e382b6535623078716b36336f754b5431
6,20,694442416e376c38726e565a576662794f587465
8,20,6c50613255726c7938356a7055746179644a6e6d
7,20,434154536d39516b4c4745673865646734457968
23,20,714b4b645969464c647050484962425079354569
20,20,424c53414a33644531534b7a597368524d327738
18,20,786e4655476f4a55307441396a4451525a414d38
12,20,7377774a6f444a7064675971796d7366366c436f
2,20,414f665867482b77514f53426741414577414141
```

We can see that the first column contains unique numbers, so we can sort the rows by the first column. Then we can see that it looks like the third column is hex encoded characters. We use python to decode it into a string and get this:

```
QlpoOTFBWSZTWWNZ3UAAAOfXgH+wQOSBgAAEwAAABEACPMDbUaEqeJJqDBqZMJNIiUnogD1CjRkDRpkaCTUKajQAaPsDqCyIMQGMiDBAn7l8rnVZWfbyOXteCATSm9QkLGEg8edg4EyhlPa2Urly85jpUtaydJnmlY6vbed52h3SIKaVNvYpt80vDOTBHLefWtm6LhZDJMgtiKJYX4spOQENWJWbswwJoDJpdgYqymsf6lCoazdp7eO+qU4WtaJbTiZMemX07gTtDiGQ8FKU8QxPeXZDyERPVtVEoNDzzJV/soSC6D4rb6MLod1uQxMwsFITcgFM3S0UiwvLvZMSxnFUGoJU0tA9jDQRZAM8vAvN8+e5b0xqk63ouKT1BLSAJ3dE1SKzYshRM2w8fbOLOw8+fLwGMOLWFf0mett113REdoLD5cFFOxrUqKKdYiFLdpPHIbBPy5EintmpipVYWrcKLRuyRTE11iVGVPUiTdgqmJIRn3K+3MS/WG7RONGfEZOoSnxa5Sof8XckU4UJBjWd1AA=
```

Looks like B64. I used [https://base64.guru/converter/decode/file](https://base64.guru/converter/decode/file) to get a file out of it.

It seems to be a BZIP file that contains another file inside of it. That file is just a txt file with the flag:

```
 _  _      __         __       ______   _             ______  __   __  __ 
| || |    / /        /_ |     |____  | | |           |____  |/ _| / _|/_ |
| || |_  / /_    __ _ | |  ___    / /__| |  ___  ______  / /| |_ | |_  | |
|__   _|| '_ \  / _` || | / _ \  / // _` | / __||______|/ / |  _||  _| | |
   | |  | (_) || (_| || ||  __/ / /| (_| || (__        / /  | |  | |   | |
   |_|   \___/  \__,_||_| \___|/_/  \__,_| \___|      /_/   |_|  |_|   |_|
                                                                          
                                                                          
         _  _    _____       __          ___   _____  ______  _____        
        | || |  | ____|     /_ |        / _ \ | ____||____  || ____|       
 ______ | || |_ | |__    ___ | | ______| (_) || |__      / / | |__  ______ 
|______||__   _||___ \  / __|| ||______|\__, ||___ \    / /  |___ \|______|
           | |   ___) || (__ | |          / /  ___) |  / /    ___) |       
           |_|  |____/  \___||_|         /_/  |____/  /_/    |____/        
                                                                           
                                                                           
 ______  _____  _____       __   ___          _____      _  __         __ 
|____  || ____|| ____|     /_ | / _ \        | ____|    | |/_ |       / _|
    / / | |__  | |__    ___ | || | | |  __ _ | |__    __| | | |  ___ | |_ 
   / /  |___ \ |___ \  / __|| || | | | / _` ||___ \  / _` | | | / __||  _|
  / /    ___) | ___) || (__ | || |_| || (_| | ___) || (_| | | || (__ | |  
 /_/    |____/ |____/  \___||_| \___/  \__,_||____/  \__,_| |_| \___||_|  
                                                                          
                                                                          
```

---
[Back to home](../README.md)
