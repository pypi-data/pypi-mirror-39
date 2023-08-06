from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

PUBLISH_KEY = 'publish'
CONTAINER_ARTIFACT_KEY = 'containerArtifact'
ADDITIONAL_TAG_KEY = 'additionalTag'

def GetInfoMsg():
    infoMsg = "Publish selections is configured by adding a 'publish' property to the .yaml file.\r\n"
    infoMsg += "The 'publish' property is a dictionary of publish selections.\r\n"
    return infoMsg


def GetPublishSelections(arguments):
    return BuildTools.GetProperties(arguments, PUBLISH_KEY, GetInfoMsg())


def PublishSelections(selectionsToPublish, publishSelections):
    if len(selectionsToPublish) == 0:
        for publishSelection in publishSelections:
            PublishSelection(publishSelections[publishSelection])
    else:
        for selectionToPublish in selectionsToPublish:
            if selectionToPublish in publishSelections:
                PublishSelection(publishSelections[selectionToPublish])


def PublishSelection(publishSelection):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(publishSelection)
    if BuildTools.TryGetFromDictionary(publishSelection, CONTAINER_ARTIFACT_KEY, True):
        PublishContainerSelection(publishSelection)
    else:
        PublishArtifactSelection(publishSelection)
    os.chdir(cwd)


def PublishContainerSelection(publishSelection):
    for composeFile in publishSelection[BuildTools.COMPOSE_FILES_KEY]:
        DockerComposeTools.PublishDockerImages(composeFile)
        if ADDITIONAL_TAG_KEY in publishSelection:
            DockerComposeTools.PublishDockerImagesWithNewTag(composeFile, publishSelection[ADDITIONAL_TAG_KEY])


def PublishArtifactSelection(publishSelection):
    DockerComposeTools.DockerComposeBuild(
        publishSelection[BuildTools.COMPOSE_FILES_KEY])
    DockerComposeTools.DockerComposeUp(
        publishSelection[BuildTools.COMPOSE_FILES_KEY], False)


def HandlePublishSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-publish' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToPublish = SwarmTools.GetArgumentValues(arguments, '-publish')
    selectionsToPublish += SwarmTools.GetArgumentValues(arguments, '-p')

    publishSelections = GetPublishSelections(arguments)
    PublishSelections(selectionsToPublish, publishSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandlePublishSelections(arguments)
