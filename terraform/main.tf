terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
      resource_group_name  = data.azurerm_resource_group.main.name
      storage_account_name = "kristinatodoappstorage"
      container_name       = "kristinatodoappcontainer"
      key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

data "azurerm_resource_group" "main" {
  name = "cohort32-33_KriSob_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "KristinaTerraformedToDoApp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name   = "8kristy/todo-app:production"
      docker_registry_url = "https://index.docker.io"
    }
  }

  app_settings = {
    "COSMOS_DB_CONNECTION_STRING"         = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    "COSMOS_DB_COLLECTION_NAME"           = azurerm_cosmosdb_mongo_collection.main.name
    "COSMOS_DB_DATABASE_NAME"             = azurerm_cosmosdb_mongo_database.main.name
    "FLASK_APP"                           = "todo_app/app"
    "OAUTH_CLIENT_ID"                     = var.oauth_client_id
    "OAUTH_CLIENT_SECRET"                 = var.oauth_client_secret
    "SECRET_KEY"                          = "secret-key"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT"                       = "5000"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                 = "kri-sob-devops-terraformed-cosmos"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  mongo_server_version = "4.2"
  offer_type           = "Standard"
  kind                 = "MongoDB"

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level = "Strong"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "to-do-app-terraformed-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_mongo_collection" "main" {
  name                = "to-do-terraformed-collection"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_mongo_database.main.name

  index {
    keys   = ["_id"]
    unique = true
  }
}