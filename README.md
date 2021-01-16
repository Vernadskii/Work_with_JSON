# Работа с JSON файлами
## Задача:
В коллекции пользователей 'Account' лежат документы вида:
```json
{
    "number": "7800000000000",
    "name": "Пользователь №1",
    "sessions": [
        {
            "created_at": "ISODate('2016-01-01T00:00:00')",
            "session_id": "6QBnQhFGgDgC2FDfGwbgEaLbPMMBofPFVrVh9Pn2quooAcgxZc",
            "actions": [
                  {
                    "type": "read",
                    "created_at": "ISODate('2016-01-01T01:20:01')"
                  },
                  {
                    "type": "read",
                    "created_at": "ISODate('2016-01-01T01:21:13')"
                  },
                  {
                    "type": "create",
                    "created_at": "ISODate('2016-01-01T01:33:59')"
                  }
               ]
            }
        ]
}
```

Необходимо написать агрегационный запрос, который по каждому пользователю выведет последнее действие и общее количество для каждого из типов 'actions'. 

Итоговые данные должны представлять собой список документов вида:
```json
{
    "number": "7800000000001",
    "actions": [
        {
          "type": "create",
          "last": null,
          "count": 0
        },
        {
          "type": "read",
          "last": null,
          "count": 0
        },
        {
          "type": "update",
          "last": null,
          "count": 0
        },
        {
          "type": "delete",
          "last": null,
          "count": 0
        }
    ]
}
```
