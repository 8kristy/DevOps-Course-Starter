param(
    [string]$DockerName,
    [string]$ResourceGroupName,
    [string]$AppServicePlanName,
    [string]$WebAppName,
    [string]$CosmosDbConnectionString,
    [string]$CosmosDbDatabaseName,
    [string]$CosmosDbCollectionName,
    [string]$OAuthClientId,
    [string]$OAuthClientSecret

)

$ImageTag = "$DockerName/todo-app:production"
docker build --target production --tag $ImageTag .
docker push $ImageTag

az appservice plan create --resource-group $ResourceGroupName -n $AppServicePlanName --sku B1 --is-linux
az webapp create --resource-group $ResourceGroupName --plan $AppServicePlanName --name $WebAppName --deployment-container-image-name docker.io/$ImageTag
az webapp config appsettings set -g $ResourceGroupName -n $WebAppName --settings FLASK=todo_app/app WEBSITE_PORT=5000 SECRET_KEY=secret-key COSMOS_DB_CONNECTION_STRING=$CosmosDbConnectionString COSMOS_DB_DATABASE_NAME=$CosmosDbDatabaseName COSMOS_DB_COLLECTION_NAME=$CosmosDbCollectionName OAUTH_CLIENT_ID=$OAuthClientId OAUTH_CLIENT_SECRET=$OAuthClientSecret
