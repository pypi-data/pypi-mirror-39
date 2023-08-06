workflow "Publish on push to master" {
  on = "push"
  resolves = ["Publish to PyPI"]
}

action "Filters for GitHub Actions" {
  uses = "actions/bin/filter@95c1a3b"
  args = "tag v*"
}

action "Publish to PyPI" {
  uses = "docker://code0x58/action-python-publish:master"
  needs = ["Filters for GitHub Actions"]
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
}
