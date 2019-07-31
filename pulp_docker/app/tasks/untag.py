from pulpcore.plugin.models import Repository, RepositoryVersion
from pulp_docker.app.models import ManifestTag


def untag_image(tag, repository_pk):
    """
    Create a new repository version without a specified manifest's tag name.
    """
    repository = Repository.objects.get(pk=repository_pk)
    latest_version = RepositoryVersion.latest(repository)

    tags_in_latest_repository = latest_version.content.filter(
        _type="docker.manifest-tag"
    )

    tags_to_remove = ManifestTag.objects.filter(
        pk__in=tags_in_latest_repository,
        name=tag
    )

    with RepositoryVersion.create(repository) as repository_version:
        repository_version.remove_content(tags_to_remove)
