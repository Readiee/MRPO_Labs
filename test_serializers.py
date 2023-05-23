from models import User, Message, GroupChat, Content
from serializers import ObjectSerializer

def test_serializer_json():
    serializer = ObjectSerializer()
    user = User(1, 'Bulat', 'bulat@mail.ru', 'password123')

    format = 'JSON'
    output_user = serializer.serialize(user, format)
    print(output_user)
    assert output_user is not None

def test_serializer_xml():
    serializer = ObjectSerializer()
    user = User(1, 'Bulat', 'bulat@mail.ru', 'password123')

    format = 'XML'
    output_user = serializer.serialize(user, format)
    print(output_user)
    assert output_user is not None