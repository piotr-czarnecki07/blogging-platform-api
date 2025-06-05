from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.utils import IntegrityError, DatabaseError, OperationalError
from baseModel.models import BlogPost
from .serializers import BlogPostSerializer
import json

@api_view(['GET'])
def getById(request, blogid: int):
    """Returns a blog post based on the ID in the database"""

    try:
        blog = BlogPost.objects.filter(id=blogid).first() # get requested blog from database
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if blog:
            serializer = BlogPostSerializer(blog, many=False) # serialize it
            return Response(serializer.data, status=status.HTTP_200_OK) # return json response to the client
        else:
            return Response({'Error': 'Bolg was not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getByTitle(request, blogtitle: str):
    """Returns a blog post based on it's title"""

    try:
        queryTitle = ''
        for letter in blogtitle:
            if letter != " ":
                queryTitle += letter
        blog = BlogPost.objects.filter(searchTitle=queryTitle).first()
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if blog:
            serializer = BlogPostSerializer(blog, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Bolg was not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def post(request):
    """Adds new blog post to the database"""

    try:
        if BlogPost.objects.filter(title=request.data.get('title')).first() is not None:
            return Response({'Error': 'Blog with such title already exists'}, status=status.HTTP_400_BAD_REQUEST)

        searchTitle = ''
        for letter in request.data.get('title'):
            if letter != " ":
                searchTitle += letter
        copy = dict(request.data)
        copy['searchTitle'] = searchTitle

        serializer = BlogPostSerializer(data=copy)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'Error': 'Could not create a blog post'}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response({'Error': 'Data could not be saved properly'}, status=status.HTTP_404_NOT_FOUND)
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update(request, blogid: int):
    """Updates existing record"""

    try:
        blog = BlogPost.objects.filter(id=blogid).first()
        if blog is None:
            return Response({'Error': 'Such blog post was not found'}, status=status.HTTP_404_NOT_FOUND)

        data = json.loads(request.body)
        blog.title = data['title']
        blog.content = data['content']
        blog.category = data['category']
        blog.tags = data['tags']

        searchTitle = ''
        for letter in data['title']:
            if letter != " ":
                searchTitle += letter
        blog.searchTitle = searchTitle
        blog.save()

        serializer = BlogPostSerializer(blog, many=False)
    except IntegrityError:
        return Response({'Error': 'Data could not be saved properly'}, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete(request, blogid: int):
    """Deletes record form database"""

    try:
        blog = BlogPost.objects.filter(id=blogid).first()
        if blog is None:
            return Response({'Error': 'Blog was not found'}, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'Status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getall(requset):
    """Returns all records form database"""

    try:
        blogs = BlogPost.objects.all()
        if len(list(blogs)) == 0:
            return Response({'Error': 'No blog posts yet'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blogs, many=True)
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getByTag(requset, tag: str):
    """Returns record from the database with a provided term"""

    try:
        results = BlogPost.objects.filter(tags__contains=[tag])
        if len(list(results)) == 0:
            return Response({'Error': 'No blog posts yet'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(results, many=True)
    except DatabaseError:
        return Response({'Error': 'Database is not avaliable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except OperationalError:
        return Response({'Error': 'Database is not configured or is overloaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)