from ariadne import ObjectType, QueryType, gql, make_executable_schema, MutationType
from ariadne.asgi import GraphQL

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
from django.contrib import auth

from car.models import Car, Category

type_defs = gql("""
    type Query {
        people: [Person!]!
        car(id: Int, price: Int): [Car!]!
        category: [Category]
        benntend: String
    }
    
    
    type Mutation {
        login(username: String!, password: String!): UsernameMutationPayload
        logout: Boolean
    }
    
    type UsernameMutationPayload {
        status: Boolean!
        user: Person
    }

    type Person {
        firstName: String
        lastName: String
        age: Int
        fullName: String
        username: String
    }
    
    type Car {
        id: Int
        name: String
        model: String
        price: Int
        category: Category
        benning: String
    }
    
    type Category {
        id: Int
        title: String
    }
""")

# Map resolver functions to Query fields using QueryType
query = QueryType()


@query.field("benntend")
def resolve_benntend(*_):
    return "Benning Is Awsome!"


# Resolvers are simple python functions
@query.field("people")
def resolve_people(*_):
    return [
        {"firstName": "John", "lastName": "Doe", "age": 21},
        {"firstName": "Bob", "lastName": "Boberson", "age": 24},
    ]


@query.field("category")
def resolve_category(*_):
    return Category.objects.all()


@query.field("car")
def resolve_car(*_, id=None, price=None):
    if id:
        return Car.objects.all().filter(pk=id)
    elif price:
        return Car.objects.all().filter(price=price)
    return Car.objects.all()


mutation = MutationType()



@mutation.field("login")
def resolve_login(_, info, username, password):
    request = info.context
    user = auth.authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return True
    return False


@mutation.field("logout")
def resolve_logout(_, info):
    request = info.context
    print(request.user)
    if request.user.is_authenticated:
        auth.logout(request)
        return True
    return False


# Map resolver functions to custom type fields using ObjectType
person = ObjectType("Person")

car = ObjectType("Car")

category = ObjectType("Category")


@person.field("username")
def resolve_username(obj, *_):
    return "%s %s" % (obj["firstName"], obj["lastName"])


# Create executable GraphQL schema
schema = make_executable_schema(type_defs, query, mutation, person, car, category)

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema, debug=True)