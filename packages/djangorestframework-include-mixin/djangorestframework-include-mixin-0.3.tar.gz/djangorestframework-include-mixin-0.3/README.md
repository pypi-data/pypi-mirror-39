# Django REST framework light includable serializer fields

## Requirements
* Python (2.7, 3.4, 3.5, 3.6)
* [Django REST Framework](https://github.com/encode/django-rest-framework) (>=3.0)


## Usage
serializers.py
```python
class GroupSerializer(SerializerIncludeMixin, ModelSerializer):
    @classproperty  # django.utils.decorators
    def extra_objects(cls):
        return {
            'users': UserSerializer(source='user_set', many=True),
            'active_users': UserSerializer(many=True),
        }

    class Meta:
        model = Group
        fields = ('id', 'name')
```

views.py
```python
class GroupViewSet(QueryOptimizerMixin, ReadOnlyModelViewSet):
    """
    Groups.

    list:
    Available includable objects:

      * users - all users;
      * active_users - only active users.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    select_related = {}
    prefetch_related = {
        'users': 'user_set',
        'active_users': Prefetch(
            lookup='user_set',
            queryset=User.objects.filter(is_active=True),
            to_attr='active_users',
        ),
    }
```

And now we can to do that:

```python
client = APIClient()
response = client.get(  # GET /groups/?include[]=active_users
    '/groups/',
    data=[
        ('include[]', 'active_users'),
    ],
)
```

This will make only 2 query: 
 * all groups
 * prefetch only active users

# Documentation
## rest_framework_include_mixin.SerializerIncludeMixin

Used in any serializer to automatically replace and add serializer fields.

### `extra_objects` class variable

**key**:str - value from GET parameter `include[]`.
For example, `profile` for `/users/?include[]=profile`.

**value**:Serializer - any field serializer.

Example:
```python
class UserSerializer(SerializerIncludeMixin, ModelSerializer):
    extra_objects =  {
        'profile': ProfileSerializer(),
        'groups': GroupSerializer(many=True),
    }

    class Meta:
        model = User
        fields = ('id', 'profile_id')
```

| GET parameters                      | Result serializer fields                                                                   |
|-------------------------------------|--------------------------------------------------------------------------------------------|
|                                     | 'id': IntegerField(), 'profile_id': IntegerField()                                         |
| ?include[]=profile                  | 'id': IntegerField(), 'profile': ProfileSerializer()                                       |
| ?include[]=groups                   | 'id': IntegerField(), 'profile_id': IntegerField(), 'groups': GroupSerializer(many=True)   |
| ?include[]=profile&include[]=groups | 'id': IntegerField(), 'profile': ProfileSerializer(), 'groups': GroupSerializer(many=True) |

*Note: standard serializer fields with/without `_id` will be replaced to field from `extra_objects`.*

*For `?include[]=profile`: `profile` and `profile_id` will be replaced to `profile` from `extra_objects`.*


## rest_framework_include_mixin.QueryOptimizerMixin

Used with ModelViewSet to optimize database queries.

### `select_related` class variable
**key**:str - value from GET parameter `include[]`.

**value**:str - field name that can be passed to select_related ([model manager function](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#select-related)).

### `prefetch_related` class variable
**key**:str - value from GET parameter `include[]`.

**value**:Union[str, Prefetch] - field name or Prefetch object that can be passed to prefetch_related ([model manager function](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#prefetch-related)).
