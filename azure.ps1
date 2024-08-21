param(
    [string]$DockerName,
    [string]$ResourceGroupName,
    [string]$AppServicePlanName,
    [string]$WebAppName,
    [string]$TrelloApiKey,
    [string]$TrelloApiToken,
    [string]$TrelloBoardId,
    [string]$TrelloToDoListId,
    [string]$TrelloDoneListId

)

$ImageTag = "$DockerName/todo-app:production"
docker build --target production --tag $ImageTag .
docker push $ImageTag

az appservice plan create --resource-group $ResourceGroupName -n $AppServicePlanName --sku B1 --is-linux
az webapp create --resource-group $ResourceGroupName --plan $AppServicePlanName --name $WebAppName --deployment-container-image-name docker.io/$ImageTag
az webapp config appsettings set -g $ResourceGroupName -n $WebAppName --settings FLASK=todo_app/app WEBSITE_PORT=5000 SECRET_KEY=secret-key TRELLO_API_KEY=$TrelloApiKey TRELLO_API_TOKEN=$TrelloApiToken TRELLO_BOARD_ID=$TrelloBoardId TRELLO_TO_DO_LIST_ID=$TrelloToDoListId TRELLO_DONE_LIST_ID=$TrelloDoneListId
