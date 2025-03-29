config_data={
    "embedding_key":"AzureOpenAIEmbedding",
    "embedding_modelid":"text-embedding-ada-002",
    "vector_db_type": "pgvector",
    "extraction_type":"chunkr",
    "schema_name":"public",
    "vector_db_config": "{dbname=postgres,user=qodeasyadmin,host=awtender.postgres.database.azure.com,password=Admin#1234,port=5432}",
    "read_source":"cloud",
    "connection_string":"DefaultEndpointsProtocol=https;AccountName=llmlayer;AccountKey=04fn1aNvVl5BouL7w6omkh2niHg93kI0tMjZ4dXbPvYFrseLOkk5FZUwuWKelrl12hsog47dQ7Ny+AStk0MD+A==;EndpointSuffix=core.windows.net",
    "company_projects_docs_connection_string":"DefaultEndpointsProtocol=https;AccountName=userinterfaceqodeasy;AccountKey=Cz/AfK+1QEBUVrgE5EgQFbP8wqttwjYDFeRXRhMGTkL2XeqmxilAeDqKJpnH4p5IZMuvfRjt33+y+AStPhBVRw==;EndpointSuffix=core.windows.net",
    "json_dir_path_local" : r"C:\Users\Rentorzo\Desktop\Qodeasy\testing_data_tender_doc", # Name of the json file directory
    "container_name" : "ocr-json-files",
    "trigger_container_name":"trigger-llm",
    "character_limit" : "5000", # Character limit for each block of text.
    "types_to_match" : "['NarrativeText','Text','Image','Header']", # Edit the types according to the requirement
    "open_api_key":"sk-svcacct-teaPs3-lGUdL3IoMUYHMRu2PnWG5X5NSKYKgUEK9DLF2UnGT3BlbkFJOYKZpyVD0Zfdv4qkJMgtwo9qOohZICsu6EhGOE2W55pLdqwA",
    "azure_api_key":"ELWDaYMXUoXIEc0SwtefIIRVbqIQot53CAkTlcYNcaXt491r5lFCJQQJ99AKACYeBjFXJ3w3AAABACOGwKam",
    "azure_endpoint":"https://awtwnder.openai.azure.com/",
    "azure_deployment_name":"gpt-4o-mini",
    "azure_api_version":"2024-08-01-preview",
    "deployment_type":"azureopenai",
    "Test_key":"test"

}