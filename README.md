# RSA Decryption Application
Please note, this script is **NOT** production ready and should not be used for real-world decryption; it may be some use or a bit of fun to view how the calculation is performed. To be able to target larger decryption strings or with larger private keys, you'll need to do some serious optimisation to be able to do anything more than basic description.

`basic_commented.py` - Designed to be a 'first attempt' at an algorithm.

`advanced_commented.py` - Designed to be a 'second attempt' that is more fancy and more refined. Unfortunately, due to time limits for the work, I was unable to fully integrate dictionaries with cross threadding.

The script takes in an array of encrypted messages, such as:
```
[
	[
		143,
		7,
        '126013031126041031041126041126098036055020036126098111098077062080080059038062084'
	]
]
```

Breaking this down:

`143` - The public key.

`7` - The encryption key.

`'126013031126041031041126041126098036055020036126098111098077062080080059038062084'` - The encrypted message.

The example above will return the decrypted message of `04/02/2020 17:10 - Message.`

I developed this script originally for the coursework of module "COMP1819" at the University of Greenwich, during which I had to provide an example of a basic algorithm that I'd programmed in Python.