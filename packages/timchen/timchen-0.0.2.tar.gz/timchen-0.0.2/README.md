# Timchen
Timchen.py utilizes the [timchen.tk api](https://timchen.tk/docs) to get random timchen images.
It can be utilized both synchronously and asynchronously.

Here is an example on how to use it asynchronously:
```py
import timchen
import asyncio

async def main():
	t = await timchen.get_random()
	print(t.url)
	print(t.description)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

And here is an example on how to use it synchronously
```py
import timchen

def main():
	t = timchen.get_random_sync()
	print(t.url)
	print(t.description)

main()
```

### Functions:
get_random(): Gets a random timchen pic
get_from_id(<id>): Gets a timchen pic from its ID
get_all(): Gets all the timchen pics as a tuple