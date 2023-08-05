from rest_framework import serializers


class Bitbucket(serializers.Serializer):
    katka_project_id = serializers.UUIDField(required=True)
    limit = serializers.IntegerField(min_value=0, required=False)
    start = serializers.IntegerField(min_value=0, required=False)


class BitbucketRepos(Bitbucket):
    project_id = serializers.CharField(required=True)
