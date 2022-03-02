### JSON reading and writing

You might also want to use JSON files, 

To load json text into a dictionary, use the `Json.loads` method.

Example:
```typescript
let json_string = "
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        ]
    }
}
";
let data = Json.loads(json_string);

Console.write(data);
```
