def unit_serializer(obj):
    return {
        "id": obj.id,
        "code": obj.code,
        "name": obj.name,
        "prefix": obj.prefix,
        "text": f"{obj.prefix} - {obj.code}"
    }
