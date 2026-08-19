"""Fail early, with the fix in the message.

The first real run of this pipeline hits a handful of environment problems that
all produce the same unhelpful shape: a Google API traceback ending in a 403 or
404 whose text does not say what to do. Each check here turns one of those into a
sentence naming the exact remedy.

Checks are ordered cheapest-first and every one is read-only.
"""

from __future__ import annotations

import logging

from google.api_core import exceptions as gexc

log = logging.getLogger(__name__)

CONSOLE = "https://console.cloud.google.com"


class PreflightError(RuntimeError):
    """A problem the user has to fix before the run can work."""


def check_project(client, project: str) -> None:
    """Confirm the BigQuery API is enabled and the project is reachable.

    A project that has never used BigQuery returns 403 with "has not been used in
    project ... before or it is disabled", which reads like a permissions problem
    and is not one.
    """
    try:
        list(client.list_datasets(project=project, max_results=1))
    except gexc.Forbidden as exc:
        message = str(exc)
        if "has not been used" in message or "is disabled" in message:
            raise PreflightError(
                f"The BigQuery API is not enabled on project {project!r}.\n"
                f"  Enable it:  gcloud services enable bigquery.googleapis.com "
                f"--project {project}\n"
                f"  or visit:   {CONSOLE}/apis/library/bigquery.googleapis.com"
                f"?project={project}"
            ) from exc
        raise PreflightError(
            f"No BigQuery access to project {project!r}. The authenticated "
            f"account needs roles/bigquery.dataEditor and roles/bigquery.jobUser.\n"
            f"  Details: {message.splitlines()[0]}"
        ) from exc
    except gexc.NotFound as exc:
        raise PreflightError(
            f"Project {project!r} not found. Check the id (not the display name) "
            f"at {CONSOLE}/home/dashboard"
        ) from exc


def check_dataset_locations(client, project: str, datasets: list[str], location: str) -> None:
    """Catch a dataset that already exists in a different region.

    BigQuery cannot join across locations, and `create_dataset` on an existing
    dataset raises Conflict, which the loader swallows. The mismatch then surfaces
    much later as a confusing "not found in location" on a query.
    """
    wrong: list[tuple[str, str]] = []
    for dataset_id in datasets:
        try:
            existing = client.get_dataset(f"{project}.{dataset_id}")
        except gexc.NotFound:
            continue
        except gexc.Forbidden:
            continue
        if existing.location and existing.location.upper() != location.upper():
            wrong.append((dataset_id, existing.location))

    if wrong:
        listed = "\n".join(f"    {name} is in {loc}" for name, loc in wrong)
        raise PreflightError(
            f"Dataset location mismatch. This run uses {location!r}, but:\n"
            f"{listed}\n"
            "  BigQuery cannot query across locations. Either re-run with "
            f"--location {wrong[0][1]}, or delete those datasets and let this "
            "run recreate them."
        )


def check_write_access(client, project: str, location: str) -> None:
    """Confirm the account can actually create a dataset, not just read.

    Read access is common and write access is not; discovering the difference
    after a long enumeration wastes the whole walk.
    """
    from google.cloud import bigquery

    probe_id = f"{project}.drive_preflight_probe"
    dataset = bigquery.Dataset(probe_id)
    dataset.location = location
    try:
        client.create_dataset(dataset)
    except gexc.Conflict:
        pass  # left over from an earlier run; that is proof enough
    except gexc.Forbidden as exc:
        raise PreflightError(
            f"The authenticated account cannot create datasets in {project!r}.\n"
            "  It needs roles/bigquery.dataEditor (to write) and "
            "roles/bigquery.jobUser (to run load jobs).\n"
            f"  Grant at: {CONSOLE}/iam-admin/iam?project={project}"
        ) from exc
    else:
        try:
            client.delete_dataset(probe_id, not_found_ok=True)
        except gexc.GoogleAPIError:
            log.debug("could not clean up the preflight probe dataset")


def check_vertex_connection(client, project: str, location: str, connection: str) -> None:
    """Confirm the Vertex connection and its IAM grant look usable.

    Only checked before the embedding stages, since everything before them works
    without Vertex.
    """
    import shutil
    import subprocess

    if not shutil.which("bq"):
        log.warning(
            "bq CLI not on PATH, so the Vertex connection cannot be verified. "
            "If embedding fails, create it with:\n"
            "  bq mk --connection --location=%s --project_id=%s "
            "--connection_type=CLOUD_RESOURCE %s",
            location, project, connection,
        )
        return

    result = subprocess.run(
        ["bq", "show", "--format=json", "--connection",
         f"{project}.{location}.{connection}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise PreflightError(
            f"No Vertex connection {project}.{location}.{connection}.\n"
            f"  Create it:  bq mk --connection --location={location} "
            f"--project_id={project} --connection_type=CLOUD_RESOURCE {connection}\n"
            "  Then grant its service account roles/aiplatform.user "
            "(the notebook's step 7 does both)."
        )


def run(loader, project: str, datasets: list[str], location: str,
        need_vertex: bool = False, connection: str = "drive_vertex") -> None:
    """Run every applicable check. Raises PreflightError with the remedy."""
    if loader.dry_run:
        log.info("[dry-run] skipping preflight")
        return

    client = loader.client
    log.info("preflight: checking project, permissions and dataset locations ...")
    check_project(client, project)
    check_write_access(client, project, location)
    check_dataset_locations(client, project, datasets, location)
    if need_vertex:
        check_vertex_connection(client, project, location, connection)
    log.info("preflight: ok")
