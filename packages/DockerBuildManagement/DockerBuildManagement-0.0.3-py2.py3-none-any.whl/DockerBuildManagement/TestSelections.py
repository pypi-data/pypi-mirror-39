from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

TEST_KEY = 'test'
TEST_CONTAINER_NAMES_KEY = 'testContainerNames'
REMOVE_TEST_CONTAINERS_KEY = 'removeTestContainers'


def GetInfoMsg():
    infoMsg = "Test selections is configured by adding a 'test' property to the .yaml file.\r\n"
    infoMsg += "The 'test' property is a dictionary of test selections.\r\n"
    return infoMsg


def GetTestSelections(arguments):
    return BuildTools.GetProperties(arguments, TEST_KEY, GetInfoMsg())


def TestSelections(selectionsToTest, testSelections):
    if len(selectionsToTest) == 0:
        for testSelection in testSelections:
            TestSelection(testSelections[testSelection])
    else:
        for selectionToTest in selectionsToTest:
            if selectionToTest in testSelections:
                TestSelection(testSelections[selectionToTest])


def TestSelection(testSelection):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(testSelection)
    DockerComposeTools.ExecuteComposeTests(
        testSelection[BuildTools.COMPOSE_FILES_KEY], 
        testSelection[TEST_CONTAINER_NAMES_KEY], 
        BuildTools.TryGetFromDictionary(testSelection, REMOVE_TEST_CONTAINERS_KEY, True))
    os.chdir(cwd)


def HandleTestSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-test' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToTest = SwarmTools.GetArgumentValues(arguments, '-test')
    selectionsToTest += SwarmTools.GetArgumentValues(arguments, '-t')

    testSelections = GetTestSelections(arguments)
    TestSelections(selectionsToTest, testSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleTestSelections(arguments)
