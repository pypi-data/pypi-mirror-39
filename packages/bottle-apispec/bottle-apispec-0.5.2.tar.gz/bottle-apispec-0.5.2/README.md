# bottle-apispec

Simple plugin to easily enable integrate Bottle, APISpec and Marshmallow.

### Example
```python
from bottle import Bottle, run
from truckpad.bottle.apispec import APISpecPlugin

app = Bottle()


class MySchema(Schema):
    id = String()
    value = String()


@app.get('/')
def index():
    """API endpoint that return MySchema
    ---
    get:
        description: API endpoint that return MySchema
        responses:
            200:
                description: It works!!!!
                schema: MySchema
    """
    data, error = MySchema.load('id', 'value')
    return data


app.install(APISpecPlugin(
    title='Example API',
    version='1.0.0',
    openapi_version='2.0',
    plugins=(
        MarshmallowPlugin(),
    ),
    scan_package='.')
)

run(app)

```