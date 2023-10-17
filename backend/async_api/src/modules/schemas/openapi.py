CACHE_HEADER = {
    "parameters": [
        {
            "name": "x-use-cache",
            "in": "header",
            "required": False,
            "schema": {
                "anyOf": [{"type": "string", "maxLength": 4}, {"type": "null"}],
                "title": "X-Use-Cache",
            },
        }
    ]
}
