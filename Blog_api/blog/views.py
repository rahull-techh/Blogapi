from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .serializers import PostSerializer
from .models import Post

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@login_required
def create_post(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        return redirect("post_list")
    return render(request, "create_post.html")


def post_list(request):

    posts = Post.objects.all()
    return render(
        request,
        "post_list.html",
        {"posts": posts}
    )


@login_required
def update_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":

        post.title = request.POST.get("title")
        post.content = request.POST.get("content")

        post.save()

        return redirect("post_list")

    return render(
        request,
        "update_post.html",
        {"post": post}
    )

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":

        post.delete()

        return redirect("post_list")

    return render(
        request,
        "delete_post.html",
        {"post": post}
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def api_post_list(request):

    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def api_post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id, author = request.user)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = PostSerializer(
            post,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "PATCH":
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        post.delete()
        return Response(status=204)